import importlib
from functools import wraps
import ramda as R
import inspect

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T


def bind(instance, func, as_name=None):
    if as_name is None:
        as_name = func.__name__
    bound_method = func.__get__(instance, instance.__class__)
    return bound_method


class SpecException(Exception):
    pass


@staticmethod
def asAllowedType(T):

    @wraps(T)
    def helper(constant=None, *args, **kwargs):

        _get0, _set0 = T(constant, *args, **kwargs)

        def _get(val, key, classee, *args, **kwargs):

            if val is not None and inspect.isclass(val):
                raise SpecException(
                    'Invalid type constant {}, should be an empty value or empty instance.'.format(constant))

            emptyInstances = _get0(val, key, classee, *args, **kwargs)
            if emptyInstances is None:
                return None
            return [i.__class__ for i in emptyInstances]

        def _set(val, key, classee, *args, **kwargs):

            if val is None:
                return _set0(val, key, classee, *args, **kwargs)

            types = []
            for v in val:
                if inspect.isclass(v):
                    v = v()
                types.append(v)

            return _set0(types, key, classee, *args, **kwargs)

        return (_get, _set)

    return helper


class Spec:
    prototypes = []

    columnSpecs = {
        'specType': {
            'transformer': T.constantNotEmpty(),
        },
        'label': {
            'transformer': T.writableEmpty(lambda val, key, classee, *args, **kwargs: None),
        },
        'required': {
            'transformer': T.writableEmpty(lambda val, key, classee, *args, **kwargs: False),
        },
        'allowedTypes': {
            'transformer': asAllowedType(T.writableEmpty)(lambda val, key, classee, *args, **kwargs: val),
        },
        'allowedValues': {
            'transformer': T.writableEmpty(lambda val, key, classee, *args, **kwargs: None),
        },
        'valueTransform': {
            'transformer': T.writableEmpty(lambda val, key, classee, *args, **kwargs: None),
        },
    }

    @staticmethod
    def errorPatch(*args, **kwargs):

        def applyMethod(method):

            @wraps(method)
            def helper(self, value, configee):
                column = method.__name__
                if not hasattr(self, column):
                    return {}
                if self[column] is None:
                    return {}

                error = method(self, value, configee)
                if error is None:
                    return {}
                return {'error': error}

            return helper

        return applyMethod

    @staticmethod
    def error(*args, **kwargs):

        def applyMethod(method):

            @wraps(method)
            def helper(self, value, configee):
                column = method.__name__
                if not hasattr(self, column):
                    return {}
                if self[column] is None:
                    return {}

                return method(self, value, configee)

            return helper

        return applyMethod

    @staticmethod
    def raiseOnError(*args, **kwargs):

        def applyMethod(method):

            @wraps(method)
            def helper(self, value, configee):
                error = method(value, configee)
                if error is not None:
                    raise SpecException(error)

            self = method.__self__
            return bind(self, helper)

        return applyMethod

    def ifEligible(*args, **kwargs):

        def applyMethod(method):

            @wraps(method)
            def helper(self, value, configee):
                column = method.__name__
                if not hasattr(self, column):
                    return None
                if self[column] is None:
                    return None

                return method(value, configee)

            self = method.__self__
            return bind(self, helper)

        return applyMethod

    @staticmethod
    def create(spec):
        specType = As(Spec)(spec)['specType']
        SpecClass = getattr(importlib.import_module(__name__), specType)
        specee = As(SpecClass)(spec)
        return specee

    @error()
    def required(self, value, configee):
        required = self['required']
        if required == True and value is None:
            return '{} is required.'.format(self['label'])
        return None

    @error()
    def allowedTypes(self, value, configee):
        allowedTypes = tuple(self['allowedTypes'])
        if None in allowedTypes and value is None:
            return None
        if (not isinstance(value, allowedTypes)):
            return '{} must be of type {}.'.format(str(value), str(self['allowedTypes']))
        return None

    @error()
    def allowedValues(self, value, configee):
        if (not value in tuple(self['allowedValues'])):
            return '{} must be one of {}.'.format(str(value), str(self['allowedValues']))
        return None

    def valueTransform(self, value, configee):
        if self['valueTransform'] is None:
            return {}

        try:
            res = self['valueTransform'](value)
        except:
            return {
                'value': value,
                'error': '{} can not be derived.'.format(str(value))
            }

        return {}

    def evaluate(self, configee):
        error = None
        value = configee['value']
        try:
            Spec.raiseOnError()(
                Spec.ifEligible()(self.allowedTypes))(value, configee)
            Spec.raiseOnError()(
                Spec.ifEligible()(self.allowedValues))(value, configee)
            Spec.raiseOnError()(
                Spec.ifEligible()(self.required))(value, configee)
            # value = self.valueTransform(value, configee)
        except SpecException as e:
            error = str(e)

        return {
            'value': value,
            'error': error,
        }


class ValueSpec(Leaf):
    prototypes = [Spec] + Spec.prototypes

    columnSpecs = {
        'specType': {
            'transformer': T.constant('ValueSpec'),
        },
    }


class CategorySpec(Leaf):
    prototypes = [Spec] + Spec.prototypes

    columnSpecs = {
        'specType': {
            'transformer': T.constant('CategorySpec'),
        },
        'valueMetas': {
            'transformer': T.writableEmpty(lambda val, key, classee, *args, **kwargs: []),
        },
        'allowedValues': {
            'transformer': T.virtual(lambda val, key, classee, *args, **kwargs:
                                     ([] if classee['required'] else [None])
                                     + list(R.map(lambda meta: meta['value'])(classee['valueMetas']))),
        },

    }


class ConfigMapSpec(Leaf):
    prototypes = [Spec] + Spec.prototypes

    columnSpecs = {
        'specType': {
            'transformer': T.constant('ConfigMapSpec'),
        },
        'allowedTypes': {
            'transformer': asAllowedType(T.constant)([dict()]),
        },
        'minCount': {
            'transformer': T.writableEmpty(lambda val, key, classee, *args, **kwargs: val if key in classee.row else None),
        },
        'maxCount': {
            'transformer': T.writableEmpty(lambda val, key, classee, *args, **kwargs: val if key in classee.row else None),
        },
    }

    @Spec.error()
    def minCount(self, value, configee):
        if (len(value) < self['minCount']):
            return '{} must have at least {} values.'.format(str(configee.specee['label']), str(self['minCount']))
        return None

    @Spec.error()
    def maxCount(self, value, configee):
        if (len(value) > self['maxCount']):
            return '{} must have at most {} values.'.format(str(configee.specee['label']), str(self['maxCount']))
        return None

    def evaluate(self, configee):
        value = configee['value']
        res = super().evaluate(configee)
        if res['error'] is not None:
            return res
        try:
            Spec.raiseOnError()(
                Spec.ifEligible()(self.minCount))(value, configee)
            Spec.raiseOnError()(
                Spec.ifEligible()(self.maxCount))(value, configee)
        except SpecException as e:
            res['error'] = str(e)

        return res
