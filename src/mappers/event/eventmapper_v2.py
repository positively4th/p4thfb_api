
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.mapper import Mapper
from src.mappers.indexmapper import IndexMapper
from src.mappers.index import Index
from src.mappers.event.eventidentifiedmapper_v2 import EventIdentifiedMapper
from src.mappers.storemapper_v2 import StoreMapper


class EventMapper(Leaf):

    prototypes = [EventIdentifiedMapper] + EventIdentifiedMapper.prototypes + \
        [StoreMapper] + StoreMapper.prototypes + \
        [IndexMapper] + IndexMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    columnSpecs = {
        'pipes': {
            'transformer': T.notEmpty(lambda val, key, classee: val),
        },
    }

    indexes = [
        {
            'table': 'events',
            'parts': [
                ['id', Index.quote],
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['file', Index.quote],
                ['__id', Index.quote],
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['file', Index.quote],
                ['possession', Index.quote, Index.cast, 'int']
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['possession', Index.quote, Index.cast, 'int']
            ]
        },
        {
            'table': 'events<-location',
            'parts': [
                ['events__id', Index.quote],
                ['__index', Index.quote],
            ]
        },
        {
            'table': 'type',
            'parts': [
                ['id', Index.quote],
            ]
        },
    ]

    queries = {
        'event':
        '''
        select 
            _e.__id, 
            _e.__id event__id, 
            cast(_e.file as text) as "matchId",
            cast(_e.id as text) as "eventId",
            cast (_e."index" as int) as "index",
            cast(_e.period as int) period,
            cast(_e.minute as int) as minute,
            cast(_e.second as int) as second,
            _e.off_camera = 'True' as "offCamera",
            _e.timestamp,
            cast(_pp.id as text) as "playPatternId",
            _pp.name as "playPatternName",
            _t.name "typeName",
            cast(_t.id as text) as "typeId",
            cast(_e.possession as int) possession,
            cast(_lx.__value as real) x,
            cast(_ly.__value as real) y,
            array[_lx.__value::real, _ly.__value::real, 1.0] p, 
            _e.out = 'True' out,
            _p.name "playerName",
            _p.id "playerId",
            cast(_ht.home_team_id as text) as "homeTeamId",
            cast(_at.away_team_id as text) as "awayTeamId",
            _ht.home_team_name as "homeTeamName",
            _at.away_team_name as "awayTeamName",
            _pt.id as "possessionTeamId",
            _pt.name as "possessionTeamName",
            _tm.id as "eventTeamId",
            _tm.name as "eventTeamName"
        from :<-filter>: as _ef
        inner join events as _e on _e.__id = _ef.__id
        left join "events<-type" _et on _et.events__id = _e.__id
        left join "type" _t on _t.__id = _et.type__id
        left join "events<-location" _elx on _elx.events__id = _e.__id and _elx.__index = 0
        left join "location" _lx on _lx.__id = _elx.location__id
        left join "events<-location" _ely on _ely.events__id = _e.__id and _ely.__index = 1
        left join "location" _ly on _ly.__id = _ely.location__id
        left join "events<-play_pattern" _epp on _epp.events__id = _e.__id
        left join "play_pattern" _pp on _pp.__id = _epp.play_pattern__id
        left join "events<-player" _ep on _ep.events__id = _e.__id
        left join "player" _p on _p.__id = _ep.player__id
        left join "matches" _m on _m.match_id = _e.file
        left join "matches<-home_team" _htm on _htm.matches__id = _m.__id
        left join "home_team" _ht on _ht.__id = _htm.home_team__id
        left join "matches<-away_team" _atm on _atm.matches__id = _m.__id
        left join "away_team" _at on _at.__id = _atm.away_team__id
        left join "events<-possession_team" _etp on _etp.events__id = _e.__id
        left join "possession_team" _pt on _pt.__id = _etp.possession_team__id
        left join "events<-team" _etm on _etm.events__id = _e.__id
        left join "team" _tm on _tm.__id = _etm.team__id
        '''
    }

    @classmethod
    def onNew(cls, self):
        pass

    def getDataQuery(self, __ids: tuple[str] | list[str]) -> tuple:
        qs = {**self.queries}
        filter = self['db'].constantRows({
            '__id': 'text',
        }, [{'__id': __id} for __id in __ids])
        qs['filter'] = filter

        q = NestedQuery.buildCTE(
            self.queries['event'], qs)
        return (q, {})
