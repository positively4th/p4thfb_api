from contrib.pyas.src.pyas_v3 import Leaf

from src.features.location.location_v2 import Location
from features.location.relativex import RelativeX as RelativeX0


class RelativeX(Leaf):

    prototypes = [
        RelativeX0, *RelativeX0.prototypes,
        Location, *Location.prototypes
    ]

    @property
    async def value(self):
        return self._value()
