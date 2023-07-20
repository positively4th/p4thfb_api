from contrib.pyas.src.pyas_v3 import Leaf

from features.location.location_v1 import Location
from features.location.relativey import RelativeY as RelativeY0


class RelativeY(Leaf):

    prototypes = [
        RelativeY0, *RelativeY0.prototypes,
        Location, *Location.prototypes,
    ]

    @property
    def value(self):
        return self._value()
