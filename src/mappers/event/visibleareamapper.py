from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.index import Index
from src.mappers.mapper import Mapper
from src.mappers.indexmapper import IndexMapper

queries = {

    'visibleArea':
    '''
            select _e.__id as event__id, _e.id as "eventId",
             _ts.*, 
             cast(_vax.__value as real) as x,
             cast(_vay.__value as real) as y,
             _tvax.__index / 2 as "index"
            from threesixty _ts
            left join events as _e on _e.id = _ts.event_uuid
            left join "threesixty<-visible_area" _tvax on _tvax.threesixty__id = _ts.__id and _tvax.__index % 2 = 0
            left join "visible_area" _vax on _vax.__id = _tvax.visible_area__id
            left join "threesixty<-visible_area" _tvay on (
             _tvay.threesixty__id = _ts.__id and _tvay.__index = _tvax.__index + 1
            )
            left join "visible_area" _vay on _vay.__id = _tvay.visible_area__id
            '''.format(),

    'filteredVisibleArea':
        '''
        select _va.*
        from :<-eventsPrimaryKeys>: as _ef
        inner join :<-visibleArea>: as _va on _va.event__id = _ef.__id
        '''.format(),

    'visibleAreaByEvent':
        '''
        select _ef.__id as event__id, array_agg(row_to_json(_va.*)) as "visibleArea"
        from :<-eventsPrimaryKeys>: as _ef
        inner join :<-filteredVisibleArea>: _va on _va.event__id = _ef.__id
        group by _ef.__id
        '''.format(),

}


class VisibleAreaMapper(Leaf):

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
                ['mod(', ['__index', Index.quote], ' , 2)'],
            ]
        },
    ]

    queries = queries

    @classmethod
    def load(cls, db, qEventsFilter, p={}, T=None):

        qVA = NestedQuery.buildTempQueries(
            queries['filteredVisibleArea'], {
                **queries,
                **{
                    'eventFilter': qEventsFilter,
                }
            }
        )

        rows = NestedQuery.query(lambda q: db.query((q, p), debug=True), qVA)
        return rows

    @classmethod
    def onNew(cls, self):
        self.row.update(queries)
