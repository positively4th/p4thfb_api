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
from mixins.event.event_v1 import Event
from src.features.feature_v1 import Feature
from src.features.wrightetal2011.spa import SPA as SPA0


class SPA:

    prototypes = [
        SPA0, *SPA0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    def value(self):
        firstEvent = As(Event)(self.event).possessionFirstEvent
        return self._value(
            None if firstEvent is None else As(Event)(firstEvent)
        )


class SPA8(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone8()
    color = 'lightcyan'


class SPA6(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone6()
    color = 'blue'


class SPA5(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone5()
    color = 'cyan'


class SPA7(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone7()
    color = 'yellow'


class SPA2(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone2()
    color = 'green'


class SPA3(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone3()
    color = 'purple'


class SPA4(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone4()
    color = 'red'


class SPA1(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone1()
    color = 'grey'
