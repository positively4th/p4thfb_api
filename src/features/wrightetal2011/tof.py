from mixins.event.eventpass import EventPass
from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011
from src.mappers.event.constants import Constants as MapperEventConstants


class TOF:

    prototypes = [
        Wrightetal2011, *Wrightetal2011.prototypes
    ]

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

    def _value(self, assistEventee, eventPass):

        def getName():

            if assistEventee is None:
                return None
            if not assistEventee['typeId'] == MapperEventConstants.passTypeId:
                return None

            # eventPass = await assistEventee['type']

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

        matchedName = getName()
        if matchedName is None:
            return None
        return 1 if matchedName == self.featureName(self.__class__) else 0

    @property
    def value(self):
        raise Exception('Not implemented.')
