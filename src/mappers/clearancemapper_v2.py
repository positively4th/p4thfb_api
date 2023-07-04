
from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.mapper_v2 import Mapper
from src.mappers.typemapper_v2 import TypeMapper


class ClearnaceMapper(Leaf):

    prototypes = [TypeMapper] + TypeMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    indexes = []

    eventType = 'clearnace'

    queries = {
        'clearnace':
        '''
        select 
        _c.__id, _c.__id clearance__id,
        _e.__id as event__id, cast(_e.id as text) as "eventId",
        _c.right_foot = 'True' as "rightFoot",
        _c.head = 'True' as head,
        _c.aerial_won = 'True' as "aerialWon",
        _c.left_foot = 'True' as "leftFoot",
        _c.other = 'True' as other,
        _bp.id "bodyPartId",
        _bp.name "bodyPartName"
        :<-filter>: _f
        inner join clearance as _c on _c.__id = _f.__id
        left join "events<-clearance" _ec on _ec.clearance__id = _c.__id
        left join "events" _e on _e.__id = _ec.events__id
        left join "clearance<-body_part" _cbp on _cbp.clearance__id = _c.__id
        left join "body_part" _bp on _bp.__id = _cbp.body_part__id

        '''
    }
