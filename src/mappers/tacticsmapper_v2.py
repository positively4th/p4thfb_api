
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.mapper_v2 import Mapper
from src.mappers.typemapper_v2 import TypeMapper


class TacticsMapper(Leaf):

    prototypes = [TypeMapper] + TypeMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    indexes = []

    eventType = 'tactics'

    queries = {
        'tactics':
        '''
        select 
        _t.__id, _t.__id tactics__id,
        _e.__id as event__id, cast(_e.id as text) as "eventId",
        cast(_t.formation as text) formation
        from :<-filter>: _f
        inner join tactics as _t on _t.__id = _f.__id
        left join "events<-tactics" _et on _et.tactics__id = _t.__id
        left join "events" _e on _e.__id = _et.events__id

        '''
    }
