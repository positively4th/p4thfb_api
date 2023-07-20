from contrib.pyas.src.pyas_v3 import Leaf

from src.features.helpers.zones import Zone1
from src.features.helpers.zones import Zone2
from src.features.helpers.zones import Zone3
from src.features.helpers.zones import Zone4
from src.features.helpers.zones import Zone5
from src.features.helpers.zones import Zone6
from src.features.helpers.zones import Zone7
from src.features.helpers.zones import Zone8
from src.features.feature_v2 import Feature
from features.wrightetal2011.pos import POS as POS0


class POS:

    prototypes = [
        POS0, *POS0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    async def value(self):
        return self._value()


class POS8(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone8()
    color = 'cyan'


class POS6(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone6()
    color = 'blue'


class POS5(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone5()
    color = 'cyan'


class POS7(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone7()
    color = 'yellow'


class POS2(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone2()
    color = 'green'


class POS3(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone3()
    color = 'purple'


class POS4(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone4()
    color = 'red'


class POS1(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone1()
    color = 'grey'
