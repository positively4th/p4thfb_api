from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import Helpers


class Player(Leaf):

    columnSpecs = {
        'actor': {
            'transformer': bool
        },
        'keeper': {
            'transformer': bool
        },
        'x': {
            'transformer': Helpers.argStripper(float, 1)
        },
        'y': {
            'transformer': Helpers.argStripper(float, 1)
        },
    }

    @classmethod
    def pipe(cls, models, filters=[]):
        res = list(models)
        for filter in filters:
            res = filter(res)
        return res

    @classmethod
    def onlyTeammates(cls, models):
        return [p for p in models if bool(p['teammate'])]

    @classmethod
    def notTeammates(cls, models):
        return [p for p in models if not bool(p['teammate'])]

    @classmethod
    def onlyFieldsers(cls, models):
        return [p for p in models if not bool(p['keeper'])]

    @classmethod
    def onlyActors(cls, models):
        return [p for p in models if bool(p['actor'])]

    @classmethod
    def notActors(cls, models):
        return [p for p in models if not bool(p['actor'])]

    @classmethod
    def onlyKeepers(cls, models):
        return [p for p in models if bool(p['keeper'])]

    @classmethod
    def notKeepers(cls, models):
        return [p for p in models if not bool(p['keeper'])]

    @property
    def p(self):
        return [self['x'], self['y'], 1]
