from contrib.pyas.src.pyas_v3 import Leaf


class EventBallReceiptMapper(Leaf):

    queries = {
        'eventBallReceiptFilter':
        '''
     select __id from ball_receipt
    ''',


        'eventBallReceipt':
        '''
    select 
    _br.__id,
    _e.__id as event__id, cast(_e.id as text) as "eventId",
    _br.file,
    _o.id as "outcomeId",
    _o.name as "outcomeName"
   
    from ball_receipt as _br
    left join "events<-ball_receipt" _ebr on _ebr.ball_receipt__id = _br.__id
    left join "events" _e on _e.__id = _ebr.events__id
    left join "ball_receipt<-outcome" _bro on _bro."ball_receipt__id" = _br."__id"
    left join "outcome" _o on _o."__id" = _bro."outcome__id"
    

    '''.format(),

        'filteredEventBallReceipt':
        '''
            select _br.*
            from :<eventBallReceiptFilter>: as _brf
            inner join :<eventBallReceipt>: as _br on _br.__id = _brf.__id
            '''.format(),
    }

    @classmethod
    def onNew(cls, self):
        pass
