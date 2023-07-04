import ramda as R

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.index import Index


class IndexMapper(Leaf):

    prototypes = []

    _indexQueryMap = None

    columnSpecs = {
        'indexes': {
            'transformer': lambda val, key, classee: val if key in classee.row else [],
        },
    }

    @classmethod
    def getQueryIndexMap(cls, indexes, quote=lambda v: v):
        res = {}
        for idx in indexes:
            q = As(Index)(idx).createQuery(quote)
            key = As(Index)(idx).name
            res[key] = q
        return res

    def ensureIndexes(self, db):
        for _, q in self.getIndexMap(db.util.quote).items():
            db.query(q)

    def getIndexMap(self, quote):
        res = {}
        for p in self.prototypes:
            if not hasattr(p, 'indexes'):
                continue
            res = R.merge(res, As(IndexMapper).getQueryIndexMap(
                p.indexes, quote=quote))
        return res
