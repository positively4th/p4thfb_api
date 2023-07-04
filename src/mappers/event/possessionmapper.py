from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.index import Index
from src.mappers.mapper import Mapper
from src.mappers.indexmapper import IndexMapper
from src.mappers.event.constants import Constants


class PossessionMapper(Leaf):

    protoypes = [Mapper] + Mapper.prototypes + \
        [IndexMapper] + IndexMapper.prototypes

    indexes = [
        {
            'table': 'events',
            'parts': [
                ['file', Index.quote]
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['index', Index.quote, Index.cast, 'int']
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['possession', Index.quote]
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['possession', Index.quote, Index.cast, 'int']
            ]
        },
        {
            # remove ?
            'table': 'events',
            'parts': [
                ['file', Index.quote],
                ['possession', Index.quote, Index.cast, 'int']
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['file', Index.quote],
                ['possession', Index.quote],
                ['index', Index.quote, Index.cast, 'int']
            ]
        },

    ]

    queries = {

        'possessionEventFilter':
        '''
    select _rpe.__id, _epks.__id as "from__id"
    from :<-eventsPrimaryKeys>: _epks
    inner join events _e on _e.__id = _epks.__id
    -- 1 to Many here since several _e rows have same possession....
    inner join events _rpe on _rpe.file = _e.file and _rpe.possession = _e.possession
    ''',


        'possessionFirstEvent':
        '''
    select _fe.__id, _fe.file, _fe.id, _fe.possession, _fe.index firstIndex
    from :<-possessionEventFilter>: _pef
    inner join events _fe on _fe.__id = _pef.__id
    left join events _pe on _pe.file = _fe.file 
      and _pe.possession = _fe.possession
      and _pe.index::int = _fe.index::int - 1 
    where _pe.__id is null
    '''.format(),

        'possessionLastEvent':
        '''
    select _le.__id, _le.file, _le.id, _le.possession, _le.index firstIndex
    from :<-possessionEventFilter>: _pef
    inner join events _le on _le.__id = _pef.__id
    left join events _fe on _fe.file = _le.file 
      and _fe.possession = _le.possession
      and _fe.index::int = _le.index::int + 1 
    where _fe.__id is null
    '''.format(),

        'xpossessionMeta':
        '''
    select _pef.__id as "events__id", _e.file, _e.possession
     , sum(
        case 
          when _t.id = '{passTypeId}' and _pt.id = _tm.id then 1
          else 0
        end
     ) over "ascPossession" 
     as "passCount"
     , sum(
        case 
          when _t.id = '{shotTypeId}'  and _pt.id = _tm.id then 1 
          else 0
        end
     ) over "ascPossession" 
     as "shotCount"
     , array_agg(
          json_build_object(
            'typeId', _t.id,
            'p', array[_lx.__value::real, _ly.__value::real, 1.0]
          )
     ) filter (
         where 1 = 1 
           --and _t.id in ('{passTypeId}', '{carryTypeId}', '{dribbledPastTypeId}') 
           and _pt.id = _tm.id
         ) 
     over "ascPossession" as locations
    from :<possessionEventFilter>: _pef
    inner join "events" as _e on _e.__id = _pef.__id 
    inner join "events<-type" "_et" on _et.events__id = _e.__id
    inner join "type" _t on _t.__id = _et.type__id
    left join "events<-possession_team" _etp on _etp.events__id = _e.__id
    left join "possession_team" _pt on _pt.__id = _etp.possession_team__id
    left join "events<-team" _etm on _etm.events__id = _e.__id
    left join "team" _tm on _tm.__id = _etm.team__id
    left join "events<-location" _elx on _elx.events__id = _e.__id and _elx.__index = 0
    left join "location" _lx on _lx.__id = _elx.location__id
    left join "events<-location" _ely on _ely.events__id = _e.__id and _ely.__index = 1
    left join "location" _ly on _ly.__id = _ely.location__id
    window "ascPossession" as (partition by _e.file, _e.possession order by _e."index"::int asc) 
    '''.format(shotTypeId=Constants.shotTypeId,
               passTypeId=Constants.passTypeId,
               interceptionTypeId=Constants.interceptionTypeId,
               carryTypeId=Constants.carryTypeId,
               duelTypeId=Constants.duelTypeId,
               clearanceTypeId=Constants.clearanceTypeId,
               goalKeeperTypeId=Constants.goalKeeperTypeId,
               dribbledPastTypeId=Constants.dribbledPastTypeId),

    }
