import numpy as np

from src.features.location.location_v2 import Location
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from mixins.event.event_v2 import Event

from constants.pitch import Pitch as P


class RelativeX(Leaf):

    prototypes = [Location] + Location.prototypes

    @property
    async def value(self):
        eventee = As(Event)(self.row)
        p = np.matmul(P.sbpTpitch, eventee.p)
        p = np.matmul(self.pitchTcentric, p)

        return 2 * p[0] / P.ext[0]
