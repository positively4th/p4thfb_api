import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from src.store.autostores import getAutoStores
from src.store.store import QueueItem
from src.store.event.eventstore import EventStore
from src.mappers.event.relatedeventsmapper_v2 import RelatedEventsMapper


class RelatedEventsStore(Leaf):

    Mapper = RelatedEventsMapper

    prototypes = [EventStore] + EventStore.prototypes

    columnSpecs = {
        'eventStore': {
            'transformer': T.virtual(lambda val, key, classee: getAutoStores()['eventStore'] if classee.eventStore is None else classee.eventStore),
        },

    }

    eventStore = None

    async def process(self, queueItems):
        db = self['db']
        mapperee = self['mapperee']
        re__ids = [As(QueueItem)(queueItem)['__id']
                   for queueItem in queueItems]

        qpT = mapperee.dataQuery(re__ids)

        relateds = await db.query(qpT)

        eventStore = self['eventStore']
        events = await eventStore.get([r['event__id'] for r in relateds])

        relateds = R.group_by(lambda r: r['__id'])(relateds)

        relateds = R.pipe(
            R.map(lambda __id: (__id, [
                {
                    **events[related['event__id']][0],
                    **{
                        'relatedEvent__id': related['__id'],
                        'event__id': related['event__id'],
                        'tag': related['tag']
                    }
                }
                for related in relateds[__id]
            ])),
            R.from_pairs
        )(re__ids)

        for queueItem in queueItems:
            __id = queueItem['__id']
            queueItemee = As(QueueItem)(queueItem)
            self.log('info', 'item {} ready to be delivered'.format(__id))
            queueItemee['result'] = relateds[__id]
        return queueItems

    async def byEvent(self, event__id: str) -> list[str]:
        mapperee = self['mapperee']
        res__id = (await mapperee.event__id2__id(event__id))[0]
        return await self.get(res__id)
