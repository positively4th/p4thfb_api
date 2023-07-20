from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from features.feature_v2 import Feature
from src.features.oppgoal.alloppgoalblockercount_v2 import AllOppGoalBlockerCount
from features.wrightetal2011.pdsg import PDSG as PDSG0


class PDSG:

    prototypes = [
        PDSG0, *PDSG0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    async def value(self):
        blockerCount = await As(AllOppGoalBlockerCount)(self.row).value
        return self._value(blockerCount)


class PDSG0_2(Leaf):
    prototypes = [PDSG] + PDSG.prototypes
    minPlayers = 0
    maxPlayers = 2


class PDSG3_5(Leaf):
    prototypes = [PDSG] + PDSG.prototypes
    minPlayers = 3
    maxPlayers = 5


class PDSG6_8(Leaf):
    prototypes = [PDSG] + PDSG.prototypes
    minPlayers = 6
    maxPlayers = 8


class PDSGAtLeast9(Leaf):
    prototypes = [PDSG] + PDSG.prototypes
    minPlayers = 9
    maxPlayers = None
