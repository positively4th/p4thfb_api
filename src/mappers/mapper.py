import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf


class Mapper(Leaf):

    prototypes = []

    queries = {}

    columnSpecs = {
        'queries': {
            'transformer': lambda val, key, classee: val if key in classee.row else {},
        },
    }

    @classmethod
    def onNew(cls, self):
        pass

    @property
    def getQueryMap(self):
        res = {}
        for p in self.prototypes:
            if not hasattr(p, 'queries'):
                continue
            res = R.merge(p.queries, res)

        return res
