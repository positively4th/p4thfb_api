import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T


from src.store.autostores import getAutoStores
from src.store.store import QueueItem
from src.store.event.eventstore import EventStore
from src.mappers.event.possessioneventsmapper_v2 import PossessionEventsMapper


class PossessionEventsStore(Leaf):

    Mapper = PossessionEventsMapper

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
        pe__ids = [As(QueueItem)(queueItem)['__id']
                   for queueItem in queueItems]

        qpT = mapperee.dataQuery(pe__ids)

        pes = await db.query(qpT)

        eventStore = self['eventStore']
        events = await eventStore.get([r['event__id'] for r in pes])

        pes = R.group_by(lambda r: r['__id'])(pes)

        pes = R.pipe(
            R.map(lambda __id: (__id, [
                {
                    **events[related['event__id']][0],
                    **{
                        'possession__id': related['__id'],
                        'event__id': related['event__id']
                    },
                }
                for related in pes[__id]
            ])),
            R.from_pairs
        )(pe__ids)

        for queueItem in queueItems:
            __id = queueItem['__id']
            queueItemee = As(QueueItem)(queueItem)
            self.log('info', 'item {} ready to be delivered'.format(__id))
            queueItemee['result'] = pes[__id]
            # events[__id] if __id in events else None
        return queueItems

    def possession__id(self, row: dict) -> str:
        return PossessionEventsMapper.possession__id(self['db'], row)

    async def byEvent(self, event__id: str) -> list[str]:
        mapperee = self['mapperee']
        res__id = (await mapperee.event__id2__id(event__id))
        assert 1 == len(res__id)
        res__id = res__id[0]
        res = await self.get(res__id)
        return res
