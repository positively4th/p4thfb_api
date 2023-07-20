from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.features.helpers.zones import Zone6Yard
from src.features.helpers.zones import Zone18Yard
from src.features.helpers.zones import ZonePitch
from src.features.feature_v1 import Feature
from src.mixins.event.event_v1 import Event
from src.features.wrightetal2011.gkp import GKP as GKP0


class GKP:

    prototypes = [
        GKP0, *GKP0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    def value(self):
        gkEvents = self.eventee.relatedGoalKeeperEvents()
        return self._value(As(Event)(gkEvents[0]) if len(gkEvents) == 1 else None)


class GKP6Yard(Leaf):
    prototypes = [GKP] + GKP.prototypes
    filterZones = [Zone6Yard]
    color = 'red'


class GKP18Yard(Leaf):
    prototypes = [GKP] + GKP.prototypes
    filterZones = [Zone18Yard, '&', '!', Zone6Yard]
    color = 'orange'


class GKPPitch(Leaf):
    prototypes = [GKP] + GKP.prototypes
    filterZones = [ZonePitch, '&', '!', Zone18Yard]
    color = 'purple'
