import numpy as np

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.features.wrightetal2011.wrightetal2011_v2 import Wrightetal2011
from src.features.helpers.zones import Zone1
from src.features.helpers.zones import Zone2
from src.features.helpers.zones import Zone3
from src.features.helpers.zones import Zone4
from src.features.helpers.zones import Zone5
from src.features.helpers.zones import Zone6
from src.features.helpers.zones import Zone7
from src.features.helpers.zones import Zone8
from mixins.event.event_v2 import Event


class SPA:

    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    @property
    async def value(self):
        try:

            p = self.event['p']

            firstEvent = await As(Event)(self.event).possessionFirstEvent
            pStart = As(Event)(firstEvent).p
            self.addMetaArea(self.zone.clockWiseZonePoints,
                             fillColor=self.color)
            self.addMetaArrow(pStart, np.subtract(p, pStart))

            return 1 if self.zone.isInZone(pStart) else 0
        except TypeError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            raise e


# def createSPA(name, zone, color='white'):

class SPA8(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone8()
    color = 'lightcyan'


class SPA6(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone6()
    color = 'blue'


class SPA5(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone5()
    color = 'cyan'


class SPA7(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone7()
    color = 'yellow'


class SPA2(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone2()
    color = 'green'


class SPA3(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone3()
    color = 'purple'


class SPA4(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone4()
    color = 'red'


class SPA1(Leaf):
    prototypes = [SPA] + SPA.prototypes
    zone = Zone1()
    color = 'grey'
