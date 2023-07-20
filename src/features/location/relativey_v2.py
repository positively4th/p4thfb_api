from contrib.pyas.src.pyas_v3 import Leaf

from src.features.location.location_v2 import Location
from features.location.relativey import RelativeY as RelativeY0


class RelativeY(Leaf):

    prototypes = [
        RelativeY0, *RelativeY0.prototypes,
        Location, *Location.prototypes,
    ]

    @property
    async def value(self):
        return self._value()
