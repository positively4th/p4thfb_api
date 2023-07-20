
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.mixins.event.event_v2 import Event
from features.wrightetal2011.tof import TOF as TOF0
from src.features.feature_v2 import Feature


class TOF:

    prototypes = [
        TOF0, *TOF0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    async def value(self):

        eventPass = None
        assistEventee = await self.eventee.assistingEvent
        assistEventee = None \
            if assistEventee is None \
            else As(Event)(assistEventee)
        if assistEventee:
            eventPass = await assistEventee['type']
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
