from contrib.pyas.src.pyas_v3 import As

from features.wrightetal2011.feed import Feed as Feed0
from mixins.event.event_v2 import Event


class Feed:

    prototypes = [
        Feed0, *Feed0.prototypes
    ]

    @property
    async def fromToPair(self):
        withinPossessionEvents = await As(Event)(self.row).withinPossessionEvents
        return self._fromToPair(withinPossessionEvents)
