
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.mapper_v2 import Mapper
from src.mappers.typemapper_v2 import TypeMapper


class CarryMapper(Leaf):

    prototypes = [TypeMapper] + TypeMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    indexes = []

    eventType = 'carry'

    queries = {
        'carry':
        '''
    select 
    _c.__id,
    _e.__id as event__id, cast(_e.id as text) as "eventId",
    cast(_elx.__value as real) "endLocationX",
    cast(_ely.__value as real) "endLocationY"
    from :<-filter>: _f
    inner join carry as _c on _c.__id = _f.__id
    left join "events<-carry" _ec on _ec.carry__id = _c.__id
    left join "events" _e on _e.__id = _ec.events__id
    left join "carry<-end_location" _celx on _celx.carry__id = _c.__id and _celx.__index = 0
    left join "carry<-end_location" _cely on _cely.carry__id = _c.__id and _cely.__index = 1
    left join "end_location" _elx on _elx.__id = _celx.end_location__id
    left join "end_location" _ely on _ely.__id = _cely.end_location__id

        '''
    }
