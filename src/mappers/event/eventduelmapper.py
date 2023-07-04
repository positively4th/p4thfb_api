from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.index import Index
from src.mappers.mapper import Mapper
from src.mappers.indexmapper import IndexMapper


class EventDuelMapper(Leaf):

    protoypes = [Mapper] + Mapper.prototypes + \
        [IndexMapper] + IndexMapper.prototypes

    indexes = []

    queries = {
        'eventDuelFilter':
        '''
     select __id from duel
    ''',


        'eventDuel':
        '''
    select _d.__id,
     _e.__id as event__id, cast(_e.id as text) as "eventId",
     cast(_t.id as int) "typeId", _t.name "typeName",
     cast(_o.id as text) "outcomeId", _o.name "outcomeName"
    from duel as _d
    left join "events<-duel" _ed on _ed.duel__id = _d.__id
    left join "events" _e on _e.__id = _ed.events__id
    left join "duel<-type" _dt on _dt.duel__id = _d.__id
    left join "type" _t on _t.__id = _dt.type__id
    left join "duel<-outcome" _do on _do.duel__id = _d.__id
    left join "outcome" _o on _o.__id = _do.outcome__id
    

    '''.format(),

        'filteredEventDuel':
        '''
    select _d.*
    from :<eventDuelFilter>: as _df
    inner join :<eventDuel>: as _d on _d.__id = _df.__id
    '''.format(),
    }

    @classmethod
    def load(cls, db, qFilter, p):
        mapperee = As(cls)()

        q = NestedQuery.buildTempQueries(
            mapperee['filteredEventDuel'], {
                **mapperee.row, **{'eventDuelFilter': qFilter, }
            }
        )
        rows = NestedQuery.query(lambda q: db.query((q, p), debug=True), q)
        return rows

    @classmethod
    def onNew(cls, self):
        pass
