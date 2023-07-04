from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.index import Index
from src.mappers.mapper import Mapper
from src.mappers.indexmapper import IndexMapper


class EventClearanceMapper(Leaf):

    protoypes = [Mapper] + Mapper.prototypes + \
        [IndexMapper] + IndexMapper.prototypes

    indexes = []

    queries = {

        'eventClearanceFilter':
        '''
     select __id from clearance
    ''',


        'eventClearance':
        '''
        select 
        _c.__id,
        _e.__id as event__id, cast(_e.id as text) as "eventId",
        _c.right_foot = 'True' as "rightFoot",
        _c.head = 'True' as head,
        _c.aerial_won = 'True' as "aerialWon",
        _c.left_foot = 'True' as "leftFoot",
        _c.other = 'True' as other,
        _bp.id "bodyPartId",
        _bp.name "bodyPartName"
        from clearance as _c
        left join "events<-clearance" _ec on _ec.clearance__id = _c.__id
        left join "events" _e on _e.__id = _ec.events__id
        left join "clearance<-body_part" _cbp on _cbp.clearance__id = _c.__id
        left join "body_part" _bp on _bp.__id = _cbp.body_part__id
     

    '''.format(),

        'filteredEventClearance':
        '''
            select _c.*
            from :<eventClearanceFilter>: as _cf
            inner join :<eventClearance>: as _c on _c.__id = _cf.__id
            '''.format(),
    }

    @classmethod
    def load(cls, db, qFilter, p):
        mapperee = As(cls)()

        q = NestedQuery.buildTempQueries(
            mapperee['filteredEventClearance'], {
                **mapperee.row, **{'eventClearanceFilter': qFilter, }
            }
        )
        rows = NestedQuery.query(lambda q: db.query((q, p), debug=True), q)
        return rows

    @classmethod
    def onNew(cls, self):
        pass
