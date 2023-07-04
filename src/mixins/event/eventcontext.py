from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.mixins.event.event import Event
from src.mixins.context.context import Context


class EventContext(Leaf):

    prototypes = [Context] + Context.prototypes

    columnSpecs = {
        'event__id': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'eventId': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }

    @classmethod
    def onNew(cls, self):
        event = self['instance']
        eventee = As(Event)(event)
        delta = Context.extendIfMissing(self.row, {
            'event__id': eventee['__id'],
            'eventId': eventee['eventId'],
        })
        for k, v in delta.items():
            self[k] = v
