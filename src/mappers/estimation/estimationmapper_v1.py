import datetime

from contrib.p4thpydb.db.sqlite.orm import ORM
from contrib.p4thpydb.db.orm import TableSpecModel
from contrib.p4thpydb.db.nestedquery import NestedQuery
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.estimation.estimationmapper import EstimationMapper as EstimationMapper0


class EstimationMapper(Leaf):

    prototypes = [EstimationMapper0] + EstimationMapper0.prototypes

    def load(self, db, estimatorIds, jiffs=None):
        orm = ORM(db)
        pipes = db.createPipes()
        orm.ensureTable(self.tableSpec)
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

        rows = NestedQuery.query(lambda q: db.query(
            (q, qpT[1], tableSpecee.Ts()), debug=True), qs)
        return rows

    def save(self, db, rows):

        now = datetime.datetime.now()
        orm = ORM(db)
        orm.ensureTable(self.tableSpec)
        for r in rows:
            if 'jiff' not in r:
                r['jiff'] = now
        orm.upsert(self.tableSpec, rows)
