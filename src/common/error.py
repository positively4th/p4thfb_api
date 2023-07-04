from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.mixins.context.context import Context


class Error(Exception):

    @staticmethod
    def errorize(ContextClasses: Context | tuple[Context] = Context, prefix: str = None):

        _prefix = '' if prefix is None else prefix + ' -> '
        _ContextClasses = ContextClasses if isinstance(
            ContextClasses, tuple) else (ContextClasses,)

        def errorize(f, *args, **kwargs):

            def errorize(self: Leaf):
                try:
                    return f(self, *args, **kwargs)
                except Exception as e:
                    raise Error(_prefix + str(e), instance=self,
                                method=f,
                                arguments=args,
                                argumentsMap=kwargs,
                                ContextClasses=_ContextClasses
                                )

            return errorize

        return errorize

    @staticmethod
    def async_errorize(ContextClasses: Context | tuple[Context] = Context, prefix: str = None):

        _prefix = '' if prefix is None else prefix + ' -> '
        _ContextClasses = ContextClasses if isinstance(
            ContextClasses, tuple) else (ContextClasses,)

        def errorize(f, *args, **kwargs):

            async def errorize(self: Leaf):
                try:
                    return await f(self, *args, **kwargs)
                except Exception as e:
                    raise Error(_prefix + str(e), instance=self,
                                method=f,
                                arguments=args,
                                argumentsMap=kwargs,
                                ContextClasses=_ContextClasses
                                )

            return errorize

        return errorize

    def __init__(self, message: str,
                 instance: Leaf = None,
                 method: callable = None,
                 arguments: tuple = None,
                 argumentsMap: dict = None,
                 context: dict = {},
                 ContextClasses: tuple[Context] = ()):
        super().__init__(message)
        self._context = context
        self._context = Context.extendIfMissing(self.context, {
            'instance': instance,
            'method': method,
            'arguments': arguments,
            'argumentsMap': argumentsMap,
            **self.context
        })
        for ContextClass in ContextClasses:
            ContextClass(self._context)

    def extend(self, context: dict):
        return Error(message=str(self), context=Context.extendIfMissing(self.context, context))

    def forJSON(self):
        return dict({
            'class': self.__class__,
            'message': str(self),
            'context': As(Context)(self._context).forJSON()
        })

    @property
    def context(self):
        return dict(self._context)
