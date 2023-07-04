from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.indexmapper import IndexMapper
from src.mappers.mapper import Mapper
from src.mappers.index import Index

queries = {

    'visiblePlayer':
        '''
         select _e.__id as event__id, _e.id as "eventId",
         _ts.__id as threesixty__id, 
	     _ff.__id as __id, 
	     _ff.teammate = 'True' as teammate, 
	     _ff.actor = 'True' as actor, 
	     _ff.keeper = 'True' as keeper, 
	     cast(_lx.__value as real) x,
	     cast(_ly.__value as real) y
         from :<-eventsPrimaryKeys>: as _ef
         inner join events _e on _e.__id = _ef.__id
         inner join threesixty _ts on _ts.event_uuid = _e.id
         left join "threesixty<-freeze_frame" _ffts on _ffts.threesixty__id = _ts.__id
         left join freeze_frame _ff on _ff.__id = _ffts.freeze_frame__id
         left join "freeze_frame<-location" _fflx on _fflx.freeze_frame__id = _ff.__id and _fflx.__index % 2 = 0  
         left join "location" _lx on _lx.__id = _fflx.location__id  
         left join "freeze_frame<-location" _ffly on _ffly.freeze_frame__id = _ff.__id and _ffly.__index = _fflx.__index + 1
         left join "location" _ly on _ly.__id = _ffly.location__id  

        '''.format(),

    'filteredVisiblePlayer':
    '''
            select _vp.*
            from :<-eventsPrimaryKeys>: as _ef
            inner join :<-visiblePlayer>: _vp on _vp.event__id = _ef.__id
            '''.format(),

    'visiblePlayerByEvent':
        '''
        select _ef.__id as event__id, array_agg(row_to_json(_vp.*)) as "visiblePlayer"
        from :<-eventsPrimaryKeys>: as _ef
        inner join :<-filteredVisiblePlayer>: _vp on _vp.event__id = _ef.__id
        group by _ef.__id
        '''.format(),

}


class VisiblePlayerMapper(Leaf):

    prototypes = [Mapper] + Mapper.prototypes + \
        [IndexMapper] + IndexMapper.prototypes

    indexes = [
        {
            'table': 'events',
            'parts': [
                ['id', Index.quote],
            ]
        },
        {
            'table': 'threesixty',
            'parts': [
                ['event_uuid', Index.quote]
            ]
        },
        {
            'table': 'freeze_frame<-location',
            'parts': [
                ['freeze_frame__id', Index.quote],
                ['mod (', ['__index', Index.quote], ' , 2)'],
            ]
        },
    ]

    queries = queries

    def load(self, db, qEventsFilter, p={}, T=None):
        self.ensureIndexes(db)

        qVA = NestedQuery.buildTempQueries(
            queries['filteredVisiblePlayer'], {
                **queries,
                **{
                    'eventFilter': qEventsFilter,
                }
            }
        )

        # print(qVA)

        rows = NestedQuery.query(lambda q: db.query((q, p), debug=True), qVA)
        return rows

    @classmethod
    def onNew(cls, self):
        self.row.update(queries)
