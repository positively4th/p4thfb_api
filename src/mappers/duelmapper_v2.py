
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.mapper_v2 import Mapper
from src.mappers.typemapper_v2 import TypeMapper


class DuelMapper(Leaf):

    prototypes = [TypeMapper] + TypeMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    indexes = []

    eventType = 'duel'

    queries = {
        'duel':
        '''
        select _d.__id, _d.__id duel__id,
        _e.__id as event__id, cast(_e.id as text) as "eventId",
        cast(_t.id as int) "typeId", _t.name "typeName",
        cast(_o.id as text) "outcomeId", _o.name "outcomeName"
        from :<-filter>: _f
        inner join duel as _d on _d.__id = _d.__id
        left join "events<-duel" _ed on _ed.duel__id = _d.__id
        left join "events" _e on _e.__id = _ed.events__id
        left join "duel<-type" _dt on _dt.duel__id = _d.__id
        left join "type" _t on _t.__id = _dt.type__id
        left join "duel<-outcome" _do on _do.duel__id = _d.__id
        left join "outcome" _o on _o.__id = _do.outcome__id
        '''
    }
