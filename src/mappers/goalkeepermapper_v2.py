
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.mapper_v2 import Mapper
from src.mappers.typemapper_v2 import TypeMapper


class GoalKeeperMapper(Leaf):

    prototypes = [TypeMapper] + TypeMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    indexes = []

    eventType = 'goalkeeper'

    queries = {
        'goalkeeper':
        '''
        select 
        _gk.__id, _gk.__id as goalkeeper__id,
        _e.__id as event__id, cast(_e.id as text) as "eventId",
        _p.name "positionName",
        cast(_t.id as text) as "goalKeeperTypeId",
        _t.name as "goalKeeperTypeName",
        cast(_elx.__value as real) "endLocationX",
        cast(_ely.__value as real) "endLocationY"
        from :<-filter>: _f
        inner join goalkeeper as _gk on _gk.__id = _f.__id
        left join "events<-goalkeeper" _egk on _egk.goalkeeper__id = _gk.__id
        left join "events" _e on _e.__id = _egk.events__id
        left join "goalkeeper<-type" _gkt on _gkt."goalkeeper__id" = _gk."__id"
        left join "type" _t on _t."__id" = _gkt."type__id"
        left join "goalkeeper<-position" _gkp on _gkp.goalkeeper__id = _gk.__id
        left join "position" _p on _p.__id = _gkp.position__id
        left join "goalkeeper<-end_location" _gkelx on _gkelx.goalkeeper__id = _gk.__id and _gkelx.__index = 0
        left join "goalkeeper<-end_location" _gkely on _gkely.goalkeeper__id = _gk.__id and _gkely.__index = 1
        left join "end_location" _elx on _elx.__id = _gkelx.end_location__id
        left join "end_location" _ely on _ely.__id = _gkely.end_location__id
        '''
    }
