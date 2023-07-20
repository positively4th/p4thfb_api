import datetime

from contrib.p4thpydb.db.orm import TableSpecModel
from contrib.p4thpydb.db.nestedquery_async import NestedQuery
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.estimation.estimationmapper import EstimationMapper as EstimationMapper0


class EstimationMapper:

    prototypes = [EstimationMapper0] + EstimationMapper0.prototypes

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
