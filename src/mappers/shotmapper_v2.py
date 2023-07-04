from contrib.pyas.src.pyas_v3 import Leaf

from src.mappers.mapper_v2 import Mapper
from src.mappers.typemapper_v2 import TypeMapper


class ShotMapper(Leaf):

    prototypes = [TypeMapper] + TypeMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    columnSpecs = {}

    indexes = []

    eventType = 'shot'

    queries = {
        'shot':
        '''
            select 
            _f.__id,
            _e.__id as event__id, cast(_e.id as text) as "eventId",
            _s.aerial_won = 'True' as "aerialWon",
            cast (_s.statsbomb_xg as real) as "xG",
            _s.first_time = 'True' as "firstTime",
            _o.name "outcomeName",
            _o.id "outcomeId",
            _t.name "typeName",
            _t.id "typeId",
            _bp.id "bodyPartId",
            _bp.name "bodyPartName",
            cast(_elx.__value as real) "endLocationX",
            cast(_ely.__value as real) "endLocationY"

            from :<-filter>: _f
            inner join shot as _s on _s.__id = _f.__id
            inner join "events<-shot" _es on _es.shot__id = _s.__id
            inner join "events" _e on _e.__id = _es.events__id
            left join "shot<-outcome" _so on _so.shot__id = _s.__id
            left join "outcome" _o on _o.__id = _so.outcome__id
            left join "shot<-type" _st on _st.shot__id = _s.__id
            left join "type" _t on _t.__id = _st.type__id
            left join "shot<-body_part" _sbp on _sbp.shot__id = _s.__id
            left join "body_part" _bp on _bp.__id = _sbp.body_part__id
            left join "shot<-end_location" _selx on _selx.shot__id = _s.__id and _selx.__index = 0
            left join "shot<-end_location" _sely on _sely.shot__id = _s.__id and _sely.__index = 1
            left join "end_location" _elx on _elx.__id = _selx.end_location__id
            left join "end_location" _ely on _ely.__id = _sely.end_location__id
        '''
    }
