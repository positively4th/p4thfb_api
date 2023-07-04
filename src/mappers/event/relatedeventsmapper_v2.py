from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.mapper_v2 import Mapper
from src.mappers.indexmapper import IndexMapper
from src.mappers.event.eventidentifiedmapper_v2 import EventIdentifiedMapper
from src.mappers.storemapper_v2 import StoreMapper
from src.mappers.index import Index
from contrib.p4thpydb.db.nestedquery import NestedQuery


class RelatedEventsMapper(Leaf):

    prototypes = [EventIdentifiedMapper] + EventIdentifiedMapper.prototypes + \
        [StoreMapper] + StoreMapper.prototypes + \
        [IndexMapper] + IndexMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    columnSpecs = {}

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
        'extendedFilter':
        '''
            select _f.__id, _e.id, _e.file, _e.possession
            from :<-filter>: _f
            inner join events _e on _e.__id = _f.__id
        ''',

        'relatedEventsHelper':
        '''
            select _pe.__id, _es.__id event__id, _es.id, _es.file, _es.possession  
              , 'shotAssisted' as tag
            from :<-extendedFilter>: _pe
            inner join "events<-pass" _ep on _ep.events__id = _pe.__id
            inner join "pass" _p on _p.__id = _ep.pass__id
            inner join "events" _es on _es.id = _p.assisted_shot_id

            union
            
            select _pe.__id, _e.__id event__id, _e.id, _e.file, _e.possession
              , 'withinPossession' as tag
            from :<-extendedFilter>: _pe
            inner join events _e on _e.file = _pe.file and _e.possession = _pe.possession 

            union
            
            select _pe.__id, _e.__id event__id, _e.id, _e.file, _e.possession
              , 'related' as tag
            from :<-extendedFilter>: _pe
            inner join "events<-related_events" _ere on _ere.events__id = _pe.__id
            inner join related_events _re on _re.__id = _ere.related_events__id
            inner join events as _e on _e.id = _re.__value

            union
            
            select _pe.__id, _pfe.__id event__id, _pfe.id, _pfe.file, _pfe.possession
              , 'possessionFirst' as tag
            from :<-extendedFilter>: _pe
            inner join :<possessionFirstEvent>: _pfe on _pfe.file = _pe.file and _pfe.possession = _pe.possession 
            
            union
            
            select _pe.__id, _ple.__id event__id, _ple.id, _ple.file, _ple.possession  
              , 'possessionLast' as tag
            from :<-extendedFilter>: _pe
            inner join :<possessionLastEvent>: _ple on _ple.file = _pe.file and _ple.possession = _pe.possession 
            
            union

            select _pe.__id, _e.__id event__id, _e.id, _e.file, _e.possession  
              , 'assistingPass' as tag
            from :<-extendedFilter>: _pe
            inner join "pass" _p on _p.assisted_shot_id = _pe.id
            inner join "events<-pass" _ep on _ep.pass__id = _p.__id
            inner join "events" _e on _e.__id = _ep.events__id 

            union
            
            select _pe.__id, _e.__id event__id, _e.id, _e.file, _e.possession  
              , 'shotKeyPass' as tag
            from :<-extendedFilter>: _pe
            inner join "events<-shot" _es on _es.events__id = _pe.__id
            inner join "shot" _s on _s.__id = _es.shot__id
            inner join "events" _e on _e.id = _s.key_pass_id
        ''',

        'relatedEvents':
        '''
        select __id, event__id, id, file, possession, array_agg(tag) tag
        from :<-relatedEventsHelper>: as _ref
        group by __id, event__id, id, file, possession  
        '''.format(),

        'possessionFirstEvent':
        '''
        select _fe.__id, _fe.file, _fe.id, _fe.possession, _fe.index firstIndex
        from :<-extendedFilter>: _pef
        inner join events _fe on _fe.file = _pef.file and _fe.possession = _pef.possession 
        left join events _pe on _pe.file = _fe.file 
          and _pe.possession = _fe.possession
          and _pe.index::int = _fe.index::int - 1 
        where _pe.__id is null
        '''.format(),

        'possessionLastEvent':
        '''
        select _le.__id, _le.file, _le.id, _le.possession, _le.index firstIndex
        from :<-extendedFilter>: _pef
        inner join events _le on _le.file = _pef.file and _le.possession = _pef.possession 
        left join events _fe on _fe.file = _le.file 
          and _fe.possession = _le.possession
          and _fe.index::int = _le.index::int + 1 
        where _fe.__id is null
        '''.format(),
    }

    @classmethod
    def onNew(cls, self):
        pass

    def getDataQuery(self, __ids) -> tuple:
        qs = {**self.queries}
        filter = self['db'].constantRows({
            '__id': 'text',
        }, [{'__id': __id} for __id in __ids])
        qs['filter'] = filter

        q = NestedQuery.buildCTE(
            self.queries['relatedEvents'], qs)
        return (q, {})
