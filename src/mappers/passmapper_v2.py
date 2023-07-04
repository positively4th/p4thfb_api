
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import Reducers

from src.mappers.mapper_v2 import Mapper
from src.mappers.typemapper_v2 import TypeMapper


class PassMapper(Leaf):

    prototypes = [TypeMapper] + TypeMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    staticReducers = {
        'queries': Reducers.parentExtends,
    }

    columnSpecs = {}

    eventType = 'pass'

    querySpecs = {
        'pass': {
            'columns': '''
            _f.__id,
            _e.__id as event__id, cast(_e.id as text) as "eventId",
            cast(_p.length as real) as length,
            _h.id as "heightId",
            _h.name as "heightName",
            _p.cut_back = 'True' as "cutBack",
            _p.no_touch = 'True' as "noTouch",
            cast (_p.angle as real) as angle,
            _p.outswinging = 'True' as "outSwinging",
            _p.through_ball = 'True' as "throughBall",
            _p.cross = 'True' as cross,
            _p.switch = 'True' as switch,
            _p.shot_assist = 'True' as "shotAssist",
            _p.file,
            _p.goal_assist = 'True' as "goalAssist",
            --_p.straight = 'True' as straight,
            _p.assisted_shot_id as "eventShotId",
            _p.aerial_won = 'True' as "aerialWon",
            cast(_elx.__value as real) "endLocationX",
            cast(_ely.__value as real) "endLocationY",
            _r.id as "recipientId",
            _r.name as "recipientName",
            _bp.id as "bodyPartId",
            _bp.name "bodyPartName",
            _t.id as "typeId",
            _t.name as "typeName",

            cast(_o.id as text) as "outcomeId",
            _o.name as "outcomeName"

            ''',

            'maybeColumns': [
                {'table': 'pass', 'column': 'miscommunication',
                 'expression': '_p.miscommunication', 'alias': 'miscommunication'},
            ],

            'tables': '''
            :<-filter>: _f
            inner join pass as _p on _p.__id = _f.__id
            inner join "events<-pass" _ep on _ep.pass__id = _p.__id
            inner join "events" _e on _e.__id = _ep.events__id
            left join "pass<-end_location" _pelx on _pelx.pass__id = _p.__id and _pelx.__index = 0
            left join "pass<-end_location" _pely on _pely.pass__id = _p.__id and _pely.__index = 1
            left join "end_location" _elx on _elx.__id = _pelx.end_location__id
            left join "end_location" _ely on _ely.__id = _pely.end_location__id
            left join "pass<-recipient" _pe on _pe.pass__id = _p.__id
            left join "recipient" _r on _r.__id = _pe.recipient__id
            left join "pass<-body_part" _pbp on _pbp.pass__id = _p.__id
            left join "body_part" _bp on _bp.__id = _pbp.body_part__id
            left join "pass<-type" _pt on _pt."pass__id" = _p."__id"
            left join "type" _t on _t."__id" = _pt."type__id"
            left join "pass<-outcome" _po on _po."pass__id" = _p."__id"
            left join "outcome" _o on _o."__id" = _po."outcome__id"
            left join "pass<-height" _ph on _ph."pass__id" = _p."__id"
            left join "height" _h on _h."__id" = _ph."height__id"
        '''
        }
    }

    indexes = []

    queries = {}
