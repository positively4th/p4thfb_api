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
from src.features.wrightetal2011.feed_v2 import Feed
from features.wrightetal2011.rof import ROF as ROF0


class ROF:

    prototypes = [
        ROF0, *ROF0.prototypes,
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


class ROF8(Leaf):
    prototypes = [ROF] + ROF.prototypes
    zone = Zone8()
    color = 'cyan'


class ROF6(Leaf):
    prototypes = [ROF] + ROF.prototypes
    zone = Zone6()
    color = 'blue'


class ROF5(Leaf):
    prototypes = [ROF] + ROF.prototypes
    zone = Zone5()
    color = 'cyan'


class ROF7(Leaf):
    prototypes = [ROF] + ROF.prototypes
    zone = Zone7()
    color = 'yellow'


class ROF2(Leaf):
    prototypes = [ROF] + ROF.prototypes
    zone = Zone2()
    color = 'green'


class ROF3(Leaf):
    prototypes = [ROF] + ROF.prototypes
    zone = Zone3()
    color = 'purple'


class ROF4(Leaf):
    prototypes = [ROF] + ROF.prototypes
    zone = Zone4()
    color = 'red'


class ROF1(Leaf):
    prototypes = [ROF] + ROF.prototypes
    zone = Zone1()
    color = 'grey'


class NOROF(Leaf):
    prototypes = [ROF] + ROF.prototypes
    zone = None
    colort = None
