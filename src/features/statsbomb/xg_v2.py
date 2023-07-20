from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v2 import Feature
from src.features.statsbomb.xg import StatsBombXG as StatsBombXG0


class StatsBombXG(Leaf):

    prototypes = [
        StatsBombXG0, *StatsBombXG0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    async def value(self):
        return self._value(await self.eventee['type'])
