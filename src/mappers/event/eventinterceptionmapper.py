from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.mapper import Mapper
from src.mappers.indexmapper import IndexMapper


class EventInterceptionMapper(Leaf):

    protoypes = [Mapper] + Mapper.prototypes + \
        [IndexMapper] + IndexMapper.prototypes

    indexes = []

    queries = {
        'eventInterceptionFilter':
        '''
     select __id from interception
    ''',


        'eventInterception':
        '''
    select 
     _i.__id,
     _e.__id as event__id, 
     cast(_e.id as text) as "eventId",
     cast(_o.id as text) "outcomeId",
     _o.name "outcomeName"
    from interception as _i
    left join "events<-interception" _ei on _ei.interception__id = _i.__id
    left join "events" _e on _e.__id = _ei.events__id
    left join "interception<-outcome" _io on _io.interception__id = _i.__id
    left join "outcome" _o on _o.__id = _io.outcome__id
    

    '''.format(),

        'filteredEventInterception':
        '''
    select _i.*
    from :<eventInterceptionFilter>: as _if
    inner join :<eventInterception>: as _i on _i.__id = _if.__id
    '''.format(),
    }

    @classmethod
    def load(cls, db, qInterceptionFilter, p):
        mapperee = As(cls)()

        qInterception = NestedQuery.buildTempQueries(
            mapperee['filteredEventInterception'], {
                **mapperee.row, **{'eventInterceptionFilter': qInterceptionFilter, }
            }
        )
        rows = NestedQuery.query(lambda q: db.query(
            (q, p), debug=True), qInterception)
        return rows

    @classmethod
    def onNew(cls, self):
        pass
