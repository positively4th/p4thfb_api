import datetime
from dill import dumps, loads

from contrib.p4thpydb.db.ts import Ts
# from contrib.p4thpydb.db.sqlite.orm import ORM
from contrib.p4thpydb.db.orm import TableSpecModel
from contrib.p4thpydb.db.nestedquery_async import NestedQuery
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.mapper import Mapper
from src.features.feature_v2 import FeatureAsStr


@staticmethod
def nullableJSON(val, inverse=False):
    if inverse:
        return val if val is None else loads(val)

    return dumps(val)


class EstimationMapper(Leaf):

    prototypes = [Mapper] + Mapper.prototypes

    tableSpec = {
        'name': 'estimation',
        'columnSpecs': {
            'jiff': {
                'definition': "TEXT NOT NULL",
                'transform': Ts.dateTimeAsStr,
            },
            'estimatorId': {
                'definition': "TEXT NOT NULL",
                'transform': Ts.str,
            },
            'XFeatureClasses': {
                'definition': "TEXT NOT NULL",
                'transform': Ts.listTCreator(FeatureAsStr),
            },
            'YFeatureClasses':  {
                'definition': "TEXT NOT NULL",
                'transform': Ts.listTCreator(FeatureAsStr),
            },
            'estimationNodes': {
                'definition': "TEXT",
                'transform': nullableJSON,
            },
            'eventIds': {
                'definition': "TEXT NOT NULL",
                'transform': Ts.json,
            },
            'state': {
                'definition': "TEXT NOT NULL",
                'transform': Ts.categoryAsStr(['running', 'failed', 'ready']),
            },
            'error': {
                'definition': "TEXT NOT NULL",
                'transform': Ts.str,
            },
        },
        'primaryKeys': ['jiff', 'estimatorId'],
    }

    queries = {

        'estimationFilter':
        '''
        select _e.estimatorId, _e.jiff
        from estimation _e
        '''.format(),

        'estimation':
        '''
        select _e.* 
        from estimation _e
        '''.format(),

        'filteredEstimation':
        '''
        select _e.* 
        from :<estimationFilter>: as _ef
        inner join :<estimation>: _e on _e.estimatorId = _ef.estimatorId and _e.jiff = _ef.jiff
        '''.format(),

    }

    async def load(self, db, estimatorIds, jiffs=None):
        orm = db.createORM(db)
        pipes = db.createPipes()
        await orm.ensureTable(self.tableSpec)
        tableSpecee = TableSpecModel(self.tableSpec)
        qpT = (
            'select jiff, estimatorId from {}'.format(self.tableSpec['name']),
            {},
            tableSpecee.Ts(),
        )
        qpT = pipes.member(qpT, 'estimatorId', estimatorIds)
        if jiffs is not None:
            qpT = pipes.member(qpT, 'jiff', jiffs)

        qs = NestedQuery.buildTempQueries('select * from :<filteredEstimation>:', {
            **self.getQueryMap,
            **{'estimationFilter': qpT[0]},
        })

        rows = await NestedQuery.query(lambda q: db.query(
            (q, qpT[1], tableSpecee.Ts()), debug=True), qs)
        return rows

    async def save(self, db, rows):
        now = datetime.datetime.now()
        orm = db.createORM(db)
        await orm.ensureTable(self.tableSpec)
        for r in rows:
            if 'jiff' not in r:
                r['jiff'] = now
        await orm.upsert(self.tableSpec, rows)
