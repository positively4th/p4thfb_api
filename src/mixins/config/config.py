
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from src.mixins.config.spec import Spec


def bind(instance, func, as_name=None):
    if as_name is None:
        as_name = func.__name__
    bound_method = func.__get__(instance, instance.__class__)
    return bound_method


class Config(Leaf):

    prototypes = []

    columnSpecs = {
        'value': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },
        'error': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },
        'spec': {
            'transformer': T.constantNotEmpty(),
        },
    }

    def evaluate(self) -> bool:

        isValid = True
        if len(self.row) < 1:
            return isValid

        specee = self.specee
        self.row.update(specee.evaluate(self))

        isValid = 'error' not in self or self['error'] is None

        if isinstance(self['value'], (tuple, list)):
            collection = enumerate(self['value'])
        elif isinstance(self['value'], dict):
            collection = self['value'].items()
            for _, childConfig in collection:
                isValid = isValid and As(Config)(childConfig).evaluate()

        return isValid

    @property
    def allConfigPaths(self) -> tuple[str]:

        res = []
        if isinstance(self['value'], dict):
            collection = self['value'].items()
            for key, childConfig in collection:
                res += [
                    [key] + kp
                    for kp in As(self.__class__)(childConfig).allConfigPaths]
        else:
            res.append([])

        return tuple(r for r in res)

    def pick(self, configPath: list[str] | tuple[str]):

        if isinstance(configPath, tuple):
            configPath = list(configPath)

        if len(configPath) < 1:
            return self['value']

        if not isinstance(self['value'], dict):
            return None

        partConfigMap = self['value']
        part = configPath.pop(0)

        if not part in partConfigMap:
            return None

        return As(Config)(partConfigMap[part]).pick(configPath)

    def materialize(self):
        specee = self.specee
        return specee.materialize(self)

    @property
    def specee(self):
        return Spec.create(self['spec'])
