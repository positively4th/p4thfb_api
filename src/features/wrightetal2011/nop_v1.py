from contrib.pyas.src.pyas_v3 import Leaf

from src.features.wrightetal2011.nop import NOP as NOP0
from src.features.feature_v1 import Feature


class NOP:

    prototypes = [
        NOP0, *NOP0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    def value(self):
        return self._value(self.eventee.withinPossessionEvents)


class NOP1to4(Leaf):
    prototypes = [NOP] + NOP.prototypes
    passesMin = 1
    passesMax = 4


class NOP5to8(Leaf):
    prototypes = [NOP] + NOP.prototypes
    passesMin = 5
    passesMax = 8


class NOP9toInfinity(Leaf):
    prototypes = [NOP] + NOP.prototypes
    passesMin = 9
    passesMax = None
