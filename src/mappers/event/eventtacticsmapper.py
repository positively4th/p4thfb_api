from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

queries = {
    'eventTacticsFilter':
    '''
     select __id from tactics
    ''',


    'eventTactics':
    '''
    select 
     _t.__id,
     _e.__id as event__id, cast(_e.id as text) as "eventId",
     cast(_o.id as text) "outcomeId", _o.name "outcomeName"
    from tactics as _t
    left join "events<-tactics" _ei on _ei.tactics__id = _t.__id
    left join "events" _e on _e.__id = _ei.events__id
    left join "tactics<-outcome" _io on _io.tactics__id = _t.__id
    left join "outcome" _o on _o.__id = _io.outcome__id
    

    '''.format(),

    'filteredEventTactics':
    '''
    select _i.*
    from :<eventTacticsFilter>: as _if
    inner join :<eventTactics>: as _i on _i.__id = _if.__id
    '''.format(),
}


class EventTacticsMapper(Leaf):

    queries = queries

    @classmethod
    def load(cls, db, qTacticsFilter, p):
        mapperee = As(cls)()

        qTactics = NestedQuery.buildTempQueries(
            mapperee['filteredEventTactics'], {
                **mapperee.row, **{'eventTacticsFilter': qTacticsFilter, }
            }
        )
        rows = NestedQuery.query(
            lambda q: db.query((q, p), debug=True), qTactics)
        return rows

    @classmethod
    def onNew(cls, self):
        self.row.update(queries)
