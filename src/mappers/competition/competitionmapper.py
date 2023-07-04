from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.mapper import Mapper


class CompetitionMapper(Leaf):

    prototypes = [Mapper] + Mapper.prototypes

    queries = {
        'competitions':
            '''
            select _c.__id
             , _c.competition_id as "competitionId"
             , _c.competition_name as "competitionName"
             , _c.country_name as "competitionCountryName"
            from competition _c
            '''.format(),
    }

    def load(self, db, *args, **kwargs):

        q = 'SELECT * FROM :<competitions>:'
        q = NestedQuery.buildCTE(q, self.getQueryMap)
        rows = NestedQuery.query(lambda q: db.query((q,), *args, **kwargs), q)
        return rows
