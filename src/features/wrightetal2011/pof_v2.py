from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.features.helpers.zones import Zone1
from src.features.helpers.zones import Zone2
from src.features.helpers.zones import Zone3
from src.features.helpers.zones import Zone4
from src.features.helpers.zones import Zone5
from src.features.helpers.zones import Zone6
from src.features.helpers.zones import Zone7
from src.features.helpers.zones import Zone8
from mixins.event.event_v2 import Event
from src.features.feature_v2 import Feature
from features.wrightetal2011.feed_v2 import Feed
from features.wrightetal2011.pof import POF as POF0


class POF:
    prototypes = [
        POF0, *POF0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    async def value(self):
        pofEvent, rofEvent, error = await As(Feed)(self.event).fromToPair
        return self._value(
            As(Event)(pofEvent) if pofEvent is not None else None,
            As(Event)(rofEvent) if rofEvent is not None else None,
            error
        )


class POF8(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone8()
    color = 'cyan'


class POF6(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone6()
    color = 'blue'


class POF5(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone5()
    color = 'cyan'


class POF7(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone7()
    color = 'yellow'


class POF2(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone2()
    color = 'green'


class POF3(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone3()
    color = 'purple'


class POF4(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone4()
    color = 'red'


class POF1(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone1()
    color = 'grey'


class NOPOF(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = None
    color = None
