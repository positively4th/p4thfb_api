import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T


class Mapper(Leaf):

    prototypes = []

    queries = {}

    columnSpecs = {
        'queries': {
            'transformer': lambda val, key, classee: val if key in classee.row else {},
        },
        'db': {
            'transformer': T.notEmpty(lambda val, key, classee: val),
        },
        'pipes': {
            'transformer': T.notEmpty(lambda val, key, classee: val),
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

    def _buildSelect(self, tables, columns, maybeColumns=[]):
        q = columns
        if len(maybeColumns) > 0:

            for colSpec in maybeColumns:
                if not self._hasColumn(colSpec['table'], colSpec['column']):
                    continue
                q = '{}, {} as {}'.format(
                    q, colSpec['expression'], colSpec['alias'])

        q = 'select {} from {}'.format(q, tables)
        return q

    def _hasColumn(self, table, column):
        db = self['db']
        tableRE = '^{}$'.format(table)
        columnRE = '^{}$'.format(column)
        columns = db.sync.query(db.columnQuery(
            tableRE=tableRE, columnRE=columnRE), fetchAll=True)
        return len(columns) > 0
