from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.common.filter import Filter
from src.mappers.mapper import Mapper


class MatchMapper(Leaf):

    prototypes = [Mapper] + Mapper.prototypes

    queries = {
        'matches':
            '''
            select 
             _m.__id
             , _m.match_id "matchId"
             , _m.match_date "matchDate"
             , cast(_m.home_score as int) "homeScore"
             , cast(_m.away_score as int) "awayScore"
             , _ht.home_team_name "homeTeamName"
             , _at.away_team_name "awayTeamName"
             , _ht.home_team_id "homeTeamId"
             , _at.away_team_id "awayTeamId"
             , _c.competition_id as "competitionId"
             , _c.competition_name as "competitionName"
             , _cs.id as "competitionStageId"
             , _cs.name as "competitionStageName"
             , (select count(*) from events _e where _m.match_id = _e.file) "eventCount"
            from matches _m
            left join "matches<-home_team" _htm on _htm.matches__id = _m.__id
            left join home_team _ht on _ht.__id = _htm.home_team__id
            left join "matches<-away_team" _atm on _atm.matches__id = _m.__id
            left join away_team _at on _at.__id = _atm.away_team__id
            left join "matches<-competition" _mc on _mc.matches__id = _m.__id
            left join competition _c on _c.__id = _mc.competition__id
            left join "matches<-competition_stage" _mcs on _mcs.matches__id = _m.__id
            left join competition_stage _cs on _cs.__id = _mcs.competition_stage__id
            where exists (select __id from events _e where _e.file = _m.match_id)
            '''.format(),
    }

    def load(self, db, filter=None):

        q = 'SELECT * FROM :<matches>:'
        p = {}

        if filter is not None:
            filteree = As(Filter)({} if filter is None else filter)
            q, p, _ = filteree.apply(db.createPipes(), (q, p))

        qs = NestedQuery.buildCTE(q, self.getQueryMap)
        rows = NestedQuery.query(lambda q: db.query((q, p)), qs)
        return rows
