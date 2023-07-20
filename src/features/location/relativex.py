import numpy as np

from contrib.pyas.src.pyas_v3 import As

from src.mixins.event.event_v2 import Event
from src.constants.pitch import Pitch as P


class RelativeX:

    prototypes = []

    def _value(self):
        eventee = As(Event)(self.row)
        p = np.matmul(P.sbpTpitch, eventee.p)
        p = np.matmul(self.pitchTcentric, p)

        return 2 * p[0] / P.ext[0]

    @property
    def value(self):
        raise Exception('Mot implemented')
