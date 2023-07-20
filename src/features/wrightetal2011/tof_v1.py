from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from mixins.event.event_v1 import Event
from features.wrightetal2011.tof import TOF as TOF0
from src.features.feature_v1 import Feature


class TOF:

    prototypes = [
        TOF0, *TOF0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    def value(self):

        eventPass = None
        assistEventee = None \
            if self.eventee.assistingEvent is None \
            else As(Event)(self.eventee.assistingEvent)
        if assistEventee:
            eventPass = assistEventee['type']
        return self._value(assistEventee, eventPass)


class TOFOpenPlayAir(Leaf):
    prototypes = [TOF] + TOF.prototypes


class TOFOpenPlayGround(Leaf):
    prototypes = [TOF] + TOF.prototypes


class TOFDeadBallAir(Leaf):
    prototypes = [TOF] + TOF.prototypes


class TOFDeadBallGround(Leaf):
    prototypes = [TOF] + TOF.prototypes


class TOFNotEvident(Leaf):
    prototypes = [TOF] + TOF.prototypes
