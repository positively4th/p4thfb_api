from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011
from mixins.event.event import Event
from mixins.event.eventshot import EventShot
from src.mappers.event.constants import Constants


class TOS:

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
    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    @property
    def value(self):

        def getName():

            eventee = As(Event)(self.event)
            if eventee['typeId'] != Constants.shotTypeId:
                return None
            eventShotee = As(EventShot)(eventee['type'])
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


class TOSFoot(Leaf):
    prototypes = [TOS] + TOS.prototypes


class TOSHead(Leaf):
    prototypes = [TOS] + TOS.prototypes


class TOSBody(Leaf):
    prototypes = [TOS] + TOS.prototypes


class TOSPenalty(Leaf):
    prototypes = [TOS] + TOS.prototypes


class TOSOther(Leaf):
    prototypes = [TOS] + TOS.prototypes
