import numpy as np

from contrib.pyas.src.pyas_v3 import As

from mixins.event.event_v2 import Event
from constants.pitch import Pitch as P


class RelativeY:

    prototypes = []

    def _value(self):
        eventee = self.eventee
        p = np.matmul(P.sbpTpitch, eventee.p)
        p = np.matmul(self.pitchTcentric, p)
        return 2 * p[1] / P.ext[1]

    @property
    async def value(self):
        raise Exception('Not implemented.')
