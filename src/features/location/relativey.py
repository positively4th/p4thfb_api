import numpy as np

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.features.location.location import Location
from src.features.feature import Feature
from mixins.event.event import Event
from constants.pitch import Pitch as P


class RelativeY(Leaf):

    prototypes = [Location, Feature]

    @property
    def value(self):
        eventee = As(Event)(self.row)
        p = np.matmul(P.sbpTpitch, eventee.p)
        p = np.matmul(self.pitchTcentric, p)
        return 2 * p[1] / P.ext[1]
