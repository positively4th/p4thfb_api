from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.index import Index
from src.mappers.mapper import Mapper
from src.mappers.indexmapper import IndexMapper


class EventCarryMapper(Leaf):

    protoypes = [Mapper] + Mapper.prototypes + \
        [IndexMapper] + IndexMapper.prototypes

    indexes = []

    queries = {
        'eventCarryFilter':
        '''
     select __id from carry
    ''',


        'eventCarry':
        '''
    select 
    _c.__id,
    _e.__id as event__id, cast(_e.id as text) as "eventId",
    cast(_elx.__value as real) "endLocationX",
    cast(_ely.__value as real) "endLocationY"
    from carry as _c
    left join "events<-carry" _ec on _ec.carry__id = _c.__id
    left join "events" _e on _e.__id = _ec.events__id
    left join "carry<-end_location" _celx on _celx.carry__id = _c.__id and _celx.__index = 0
    left join "carry<-end_location" _cely on _cely.carry__id = _c.__id and _cely.__index = 1
    left join "end_location" _elx on _elx.__id = _celx.end_location__id
    left join "end_location" _ely on _ely.__id = _cely.end_location__id
    

    '''.format(),

        'filteredEventCarry':
        '''
            select _c.*
            from :<eventCarryFilter>: as _cf
            inner join :<eventCarry>: as _c on _c.__id = _cf.__id
            '''.format(),

    }

    @classmethod
    def load(cls, db, qCarryFilter, p):
        mapperee = As(cls)()

        qCarry = NestedQuery.buildTempQueries(
            mapperee['filteredEventCarry'], {
                **mapperee.row, **{'eventCarryFilter': qCarryFilter, }
            }
        )
        rows = NestedQuery.query(
            lambda q: db.query((q, p), debug=True), qCarry)
        return rows

    @classmethod
    def onNew(cls, self):
        pass
