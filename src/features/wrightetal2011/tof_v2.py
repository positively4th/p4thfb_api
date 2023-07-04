
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.features.wrightetal2011.wrightetal2011_v2 import Wrightetal2011
from mixins.event.event_v2 import Event
from mixins.event.eventpass import EventPass
from src.mappers.event.constants import Constants as MapperEventConstants


class TOF:

    nameMatchers = [
        {
            'name': 'TOFDeadBallAir',
            'heightId': [EventPass.lowHeightId, EventPass.highHeightId],
            'typeId': [EventPass.cornerTypeId, EventPass.freeKickTypeId, EventPass.goalKickTypeId,
                       EventPass.kickOfTypeId, EventPass.throwInTypeId],
        },
        {
            'name': 'TOFDeadBallGround',
            'heightId': [EventPass.groundHeightId],
            'typeId': [EventPass.cornerTypeId, EventPass.freeKickTypeId, EventPass.goalKickTypeId,
                       EventPass.kickOfTypeId, EventPass.throwInTypeId],
        },
        {
            'name': 'TOFOpenPlayAir',
            'heightId': [EventPass.lowHeightId, EventPass.highHeightId],
        },
        {
            'name': 'TOFOpenPlayGround',
            'heightId': [EventPass.groundHeightId],
        },
        {
            'name': 'TOFNotEvident',
        },

    ]
    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    @property
    async def value(self):

        async def getName():

            Eventee = As(Event)(self.event)

            assistingEvent = await Eventee.assistingEvent
            assistEventee = None \
                if assistingEvent is None \
                else As(Event)(assistingEvent)
            if assistEventee is None:
                return None
            if not assistEventee['typeId'] == MapperEventConstants.passTypeId:
                return None

            eventPass = await assistEventee['type']

            for matcher in self.nameMatchers:
                name = matcher['name']
                for key, values in matcher.items():
                    if key == 'name':
                        name = matcher['name']
                        continue
                    if not key in eventPass:
                        name = None
                        break
                    if not eventPass[key] in values:
                        name = None
                        break
                if name is not None:
                    return name

        matchedName = await getName()
        if matchedName is None:
            return None
        return 1 if matchedName == self.featureName(self.__class__) else 0


class TOFOpenPlayAir(Leaf):
    prototypes = [TOF] + TOF.prototypes


class TOFOpenPlayGround(Leaf):
    prototypes = [TOF] + TOF.prototypes


class TOFDeadBallAir(Leaf):
    prototypes = [TOF] + TOF.prototypes


class TOFDeaBallGround(Leaf):
    prototypes = [TOF] + TOF.prototypes


class TOFNotEvident(Leaf):
    prototypes = [TOF] + TOF.prototypes
