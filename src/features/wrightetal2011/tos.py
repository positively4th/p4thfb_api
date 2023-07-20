from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011
from src.mixins.event.eventshot import EventShot
from src.mappers.event.constants import Constants


class TOS:

    prototypes = [Wrightetal2011, *Wrightetal2011.prototypes]

    nameMatchers = [
        {
            'name': 'TOSPenalty',
            'typeId': [EventShot.penaltyTypeId],
        },
        {
            'name': 'TOSFoot',
            'bodyPartId': [EventShot.bodyPartId['leftFoot'], EventShot.bodyPartId['rightFoot']],
        },
        {
            'name': 'TOSHead',
            'bodyPartId': [EventShot.bodyPartId['head']],
        },
        {
            'name': 'TOSBody',
            'bodyPartId': [EventShot.bodyPartId['other']],
        },
        {
            'name': 'TOSOther',
        },

    ]

    def _value(self, eventShotee):

        def getName():

            eventee = self.eventee
            if eventee['typeId'] != Constants.shotTypeId:
                return None
            for matcher in self.nameMatchers:
                name = matcher['name']
                for key, values in matcher.items():
                    if key == 'name':
                        name = matcher['name']
                        continue
                    if not key in eventShotee:
                        name = None
                        break
                    if not eventShotee[key] in values:
                        name = None
                        break
                if name is not None:
                    return name

        matchedName = getName()
        if matchedName is None:
            return None
        return 1 if matchedName == self.featureName(self.__class__) else 0

    @property
    async def value(self):
        raise Exception('Not implemented.')
