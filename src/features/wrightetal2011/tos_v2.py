from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.mixins.event.eventshot import EventShot
from features.wrightetal2011.tos import TOS as TOS0
from src.features.feature_v2 import Feature


class TOS:

    prototypes = [
        TOS0, *TOS0.prototypes,
        Feature, *Feature.prototypes
    ]

    @property
    async def value(self):
        eventShot = await self.eventee['type']
        return self._value(
            None if eventShot is None else As(EventShot)(eventShot)
        )


class TOSFoot(Leaf):
    prototypes = [TOS] + TOS.prototypes


class TOSHead(Leaf):
    prototypes = [TOS] + TOS.prototypes


class TOSBody(Leaf):
    prototypes = [TOS] + TOS.prototypes


class TOSPenalty(Leaf):
    prototypes = [TOS] + TOS.prototypes


class TOSOther(Leaf):
    prototypes = [TOS] + TOS.prototypes
