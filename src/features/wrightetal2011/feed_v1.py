from contrib.pyas.src.pyas_v3 import As

from features.wrightetal2011.feed import Feed as Feed0
from mixins.event.event_v1 import Event


class Feed:

    prototypes = [
        Feed0, *Feed0.prototypes
    ]

    @property
    def fromToPair(self):
        return self._fromToPair(As(Event)(self.row).withinPossessionEvents)
