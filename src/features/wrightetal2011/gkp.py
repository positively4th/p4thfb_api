from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011
from src.features.helpers.zones import Zone6Yard
from src.features.helpers.zones import Zone18Yard
from src.features.helpers.zones import ZonePitch
from constants.statsbombpitch import StatsBombPitch as SBP
from mixins.event.event import Event
from src.tools.matcher import Matcher
from src.tools.color import Color


def transform(what, T):

    if isinstance(what, (tuple, list)):
        return [T(w) for w in what]

    if isinstance(what, dict):
        return {k: T(v) for k, v in what.items()}

    return T(what)


class GKP:
    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    @classmethod
    def onNew(cls, self):

        def createDrawZone(zone):

            def drawZone(_, sign):
                c = self.color if sign == 1 else Color.complement(self.color)
                self.addMetaArea(zone.clockWiseZonePoints, c)

            return drawZone

        self.isMatchFilter = transform(
            self.filterZones, lambda torz: torz.isInZone if hasattr(torz, 'isInZone') else torz)
        self.zoneAddMeta = transform(self.filterZones, lambda torz: createDrawZone(
            torz) if hasattr(torz, 'isInZone') else torz)

    @property
    def value(self):
        try:
            eventee = As(Event)(self.event)
            if not eventee.isGoalKeeperEvent():
                gkEvent = eventee.relatedGoalKeeperEvents()
                assert len(gkEvent) == 1
                eventee = As(Event)(gkEvent[0])

            p = eventee['p']
            if eventee['possessionTeamId'] != eventee['eventTeamId']:
                p = [
                    SBP.sbRightOppCorner[0] - p[0],
                    SBP.sbRightOppCorner[1] - p[1],
                    1,
                ]
            self.addMetaAnnotation(p, 'GK')

            Matcher.traverse(p, self.zoneAddMeta)

            return 1 if Matcher.isMatch(p, self.isMatchFilter) else 0
        except TypeError as e:
            return None
        except Exception as e:
            print(e)
            raise e


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
