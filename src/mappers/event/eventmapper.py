import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.mapper import Mapper
from src.mappers.indexmapper import IndexMapper
from src.mappers.index import Index
from src.mappers.event.visibleareamapper import VisibleAreaMapper
from src.mappers.event.visibleplayermapper import VisiblePlayerMapper
from src.mappers.event.eventcarrymapper import EventCarryMapper
from src.mappers.event.eventduelmapper import EventDuelMapper
from src.mappers.event.eventgoalkeepermapper import EventGoalKeeperMapper
from src.mappers.event.eventpassmapper import EventPassMapper
from src.mappers.event.eventshotmapper import EventShotMapper
from src.mappers.event.eventclearancemapper import EventClearanceMapper
from src.mappers.event.eventinterceptionmapper import EventInterceptionMapper
from src.mappers.event.possessionmapper import PossessionMapper as EventPossessionMapper
from src.mappers.event.eventballreceiptmapper import EventBallReceiptMapper
from src.mappers.event.constants import Constants


class EventMapper(Leaf):

    prototypes = [EventShotMapper] + EventShotMapper.prototypes \
        + [EventPassMapper] + EventPassMapper.prototypes \
        + [EventInterceptionMapper] + EventInterceptionMapper.prototypes \
        + [EventCarryMapper] + EventCarryMapper.prototypes \
        + [EventDuelMapper] + EventDuelMapper.prototypes \
        + [EventPossessionMapper] + EventPossessionMapper.prototypes \
        + [EventClearanceMapper] + EventClearanceMapper.prototypes \
        + [EventGoalKeeperMapper] + EventGoalKeeperMapper.prototypes \
        + [EventBallReceiptMapper] + EventBallReceiptMapper.prototypes \
        + [VisiblePlayerMapper] + VisiblePlayerMapper.prototypes \
        + [VisibleAreaMapper] + VisibleAreaMapper.prototypes \
        + [Mapper] + Mapper.prototypes + [IndexMapper] + IndexMapper.prototypes

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

        'eventFilter':
        '''
        with recursive x(from__id, __id, id, file, possession) as  (
          select null as from__id, _espk.__id, _e.id, _e.file, _e.possession, cast('root' as text) as tag
            , row_number() over () as __order
          from :<eventsPrimaryKeys>: _espk
          inner join events _e on _e.__id = _espk.__id
        
          union
                 
          select _e.from__id, _e.__id, _e.id, _e.file, _e.possession, tag, cast (null as int) as __order
          from (
         
            with _pe as (
             select * from x
            )
            
            select _pe.__id as from__id, _e.__id, _e.id, _e.file, _e.possession
              , 'withinPossession' as tag
            from _pe
            inner join :<-possessionEventFilter>: _pef on _pef.from__id = _pe.__id 
            inner join events _e on _e.__id = _pef.__id 

            union
            
            select _ere.events__id as from__id, _e.__id, _e.id, _e.file, _e.possession
              , 'related' as tag
            from _pe
            inner join "events<-related_events" _ere on _ere.events__id = _pe.__id
            inner join related_events _re on _re.__id = _ere.related_events__id
            inner join events as _e on _e.id = _re.__value

            union
            
            select _pe.__id as from__id, _pfe.__id, _pfe.id, _pfe.file, _pfe.possession
              , 'possessionFirst' as tag
            from _pe
            inner join :<possessionFirstEvent>: _pfe on _pfe.file = _pe.file and _pfe.possession = _pe.possession 
            
            union
            
            select _pe.__id as "from__id", _ple.__id, _ple.id, _ple.file, _ple.possession  
              , 'possessionLast' as tag
            from _pe
            inner join :<possessionFirstEvent>: _ple on _ple.file = _pe.file and _ple.possession = _pe.possession 
            
            union

            select _pe.__id as "from__id", _es.__id, _es.id, _es.file, _es.possession  
              , 'shotAssisted' as tag
            from _pe
            inner join "events<-pass" _ep on _ep.events__id = _pe.__id
            inner join "pass" _p on _p.__id = _ep.pass__id
            inner join "events" _es on _es.id = _p.assisted_shot_id

            union
            
            select _pe.__id as "from__id", _e.__id, _e.id, _e.file, _e.possession  
              , 'assistingPass' as tag
            from _pe
            inner join "pass" _p on _p.assisted_shot_id = _pe.id
            inner join "events<-pass" _ep on _ep.pass__id = _p.__id
            inner join "events" _e on _e.__id = _ep.events__id 

            union
            
            select _pe.__id as "from__id", _e.__id, _e.id, _e.file, _e.possession  
              , 'shotKeyPass' as tag
            from _pe
            inner join "events<-shot" _es on _es.events__id = _pe.__id
            inner join "shot" _s on _s.__id = _es.shot__id
            inner join "events" _e on _e.id = _s.key_pass_id

         ) _e
         --left join :<eventsPrimaryKeys>: _sef on _sef.__id = _e.__id
         --where _sef.__id is null
        ) 
        select *
        from x as _ref
        --order by _ref."from__id" is null desc, _ref.__order asc
        ''',

        'event':
            '''
    select 
     _e.__id, 
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
     _tm.name as "eventTeamName",
     _va."visibleArea",
     _vp."visiblePlayer" as "visiblePlayers",
     row_to_json(coalesce(
      _shot.*, 
      _pass.*, 
      _interception.*, 
      _carry.*, 
      _duel.*,
      _clearance.*,
      "_goalKeeper".*,
      "_ballReceipt".*
      )) as "type"
    from :<-eventsPrimaryKeys>: as _espk
    inner join events as _e on _e.__id = _espk.__id
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
    left join :<-visibleAreaByEvent>: _va on _va.event__id = _e.__id
    left join :<-visiblePlayerByEvent>: _vp on _vp.event__id = _e.__id
    left join :<-eventShot>: _shot on _t.id = '{shotTypeId}' and _shot.event__id = _e.__id
    left join :<-eventPass>: _pass on _t.id = '{passTypeId}' and _pass.event__id = _e.__id
    left join :<-eventInterception>: _interception on _t.id = '{interceptionTypeId}' and _interception.event__id = _e.__id
    left join :<-eventCarry>: _carry on _t.id = '{carryTypeId}' and _carry.event__id = _e.__id
    left join :<-eventDuel>: _duel on _t.id = '{duelTypeId}' and _duel.event__id = _e.__id
    left join :<-eventClearance>: _clearance on _t.id = '{clearanceTypeId}' and _clearance.event__id = _e.__id
    left join :<-eventGoalKeeper>: "_goalKeeper" on _t.id = '{goalKeeperTypeId}' and "_goalKeeper".event__id = _e.__id
    left join :<-eventBallReceipt>: "_ballReceipt" on "_ballReceipt".event__id = _e.__id
    '''.format(shotTypeId=Constants.shotTypeId,
               passTypeId=Constants.passTypeId,
               interceptionTypeId=Constants.interceptionTypeId,
               carryTypeId=Constants.carryTypeId,
               duelTypeId=Constants.duelTypeId,
               clearanceTypeId=Constants.clearanceTypeId,
               goalKeeperTypeId=Constants.goalKeeperTypeId,
               ballReceiptTypeId=Constants.ballReceiptTypeId),
    }

    @classmethod
    def onNew(cls, self):
        pass

    def load(self, db, qpTFilter, batchSize=1000):
        self.ensureIndexes(db)

        q, p, T = db.util.qpTSplit(qpTFilter)
        qEventsPrimaryKeys = q

        qEventFilter = '''
        select * from :<eventFilter>:
        '''
        qs = {
            **self.getQueryMap,
            **{
                'eventsPrimaryKeys': qEventsPrimaryKeys,
            },
        }

        rows = self.queryNested(db, qEventFilter, qs, p)
        relatedRows = [r for r in rows]
        ids = R.uniq([r['__id'] for r in relatedRows])
        resultRows = [r for r in relatedRows if r['__order'] is not None]

        idEventMap = {}
        while True:
            batch = ids[0:batchSize]
            if len(batch) < 1:
                break
            print('Querying for {} events ...'.format(
                len(batch)), flush=True, end='')
            idEventMap.update(self.load__ids(db, batch))
            print('done '.format(batchSize), flush=True)
            del ids[0:batchSize]

        for rr in R.filter(lambda rr: rr['from__id'] is not None)(relatedRows):
            event = idEventMap[rr['from__id']]
            if 'relatedEvents' not in event:
                event['relatedEvents'] = {}
            relatedEvents = event['relatedEvents']
            if rr['tag'] not in relatedEvents:
                relatedEvents[rr['tag']] = []
            relatedEvents[rr['tag']].append(idEventMap[rr['__id']])

        return [idEventMap[rr['__id']] for rr in resultRows]

    def load__ids(self, db, filtereds):

        qEventFilter = 'select distinct __id from (values {}) as _ ("__id")'.format(
            ', '.join(["('{}')".format(f) for f in filtereds])
        )
        qs = {
            **self.getQueryMap,
            **{
                'eventsPrimaryKeys': qEventFilter,
            },
        }
        rows = self.queryNested(db,
                                'select _e.* from :<-eventsPrimaryKeys>: _ef inner join :<-event>: as _e on _e.__id = _ef.__id', qs, {})
        rows = [r for r in rows]
        if len(rows) < 1:
            return []

        idEventMap = R.index_by(
            lambda row: row['__id']
        )(rows)

        return idEventMap

    @classmethod
    def queryNested(cls, db, q, qs, p, useCTE=True):
        if useCTE:
            qNested = NestedQuery.buildCTE(q, qs)
            # print(qNested)
            rows = db.query((qNested, p))
        else:
            qNested = NestedQuery.buildTempQueries(
                q, qs
            )
            rows = NestedQuery.query(
                lambda q: db.query((q, p), debug=False), qNested)

        return rows
