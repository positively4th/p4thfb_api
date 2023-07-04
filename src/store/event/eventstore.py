
from contrib.pyas.src.pyas_v3 import Leaf

from src.store.store import Store
from src.mappers.event.eventmapper_v2 import EventMapper


class EventStore(Leaf):

    Mapper = EventMapper

    prototypes = [Store] + Store.prototypes
