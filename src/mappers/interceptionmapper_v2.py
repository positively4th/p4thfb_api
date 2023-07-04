
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.mapper_v2 import Mapper
from src.mappers.typemapper_v2 import TypeMapper


class InterceptionMapper(Leaf):

    prototypes = [TypeMapper] + TypeMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    indexes = []

    eventType = 'interception'

    queries = {
        'interception':
        '''
        select 
        _i.__id, _i.__id as interception__id,
        _e.__id as event__id, 
        cast(_e.id as text) as "eventId",
        cast(_o.id as text) "outcomeId",
        _o.name "outcomeName"
        from :<-filter>: _f
        inner join interception as _i on _i.__id = _f.__id
        left join "events<-interception" _ei on _ei.interception__id = _i.__id
        left join "events" _e on _e.__id = _ei.events__id
        left join "interception<-outcome" _io on _io.interception__id = _i.__id
        left join "outcome" _o on _o.__id = _io.outcome__id
        '''
    }
