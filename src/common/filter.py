from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.pipes import Pipes
from src.mappers.event.constants import Constants


class Filter(Leaf):

    eventFilter = '''
    select 
     _e.__id, 
     _e.id,
     _e.file,
     _e.possession,
     _t.id as "typeId",
     _e.file as "matchId",
     _e.index::int as index,
     _e.period::int period,
     _e.minute::int as minute,
     _e.second::int as second,
     _pp.id as "playPatternId",
     _e.timestamp 
    from events as _e
    left join "events<-type" _et on _et.events__id = _e.__id
    left join "type" _t on _t.__id = _et.type__id
    left join "events<-play_pattern" _epp on _epp.events__id = _e.__id
    left join "play_pattern" _pp on _pp.__id = _epp.play_pattern__id
    
    '''.format(shotTypeId=Constants.shotTypeId,
               passTypeId=Constants.passTypeId,
               interceptionTypeId=Constants.interceptionTypeId,
               carryTypeId=Constants.carryTypeId,
               duelTypeId=Constants.duelTypeId,
               clearanceTypeId=Constants.clearanceTypeId,
               goalKeeperTypeId=Constants.goalKeeperTypeId,
               ballReceiptTypeId=Constants.ballReceiptTypeId)

    def apply(self, pipes: Pipes, qpT):

        def applyColumnFilter(cF: dict, qpT):
            op = cF['op'] if 'op' in cF else '='
            values = cF['values'] if 'values' in cF else []
            column = cF['column']
            return pipes.member(qpT, column, values, op=op, quote=None)

        def applyOrder(os, qpT):
            exprs = []
            orders = []
            for o in os:
                if isinstance(o, str):
                    exprs.append(o)
                    orders.append('ASC')
                else:
                    exprs.append(o[0])
                    orders.append(o[1] if len(o) > 1 else 'ASC')
            return pipes.order(qpT, exprs, orders, quote=None)

        if 'columnFilter' in self:
            for cF in self['columnFilter']:
                qpT = applyColumnFilter(cF, qpT)

        if 'order' in self:
            qpT = applyOrder(self['order'], qpT)

        if 'limit' in self or 'offset' in self:
            qpT = pipes.limit(qpT,
                              limit=self['limit'] if 'limit' in self else None,
                              offset=self['offset'] if 'offset' in self else None)

        return qpT
