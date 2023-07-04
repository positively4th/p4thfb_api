
from contrib.pyas.src.pyas_v3 import Leaf

from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011
from src.features.helpers.zones import Zone1
from src.features.helpers.zones import Zone2
from src.features.helpers.zones import Zone3
from src.features.helpers.zones import Zone4
from src.features.helpers.zones import Zone5
from src.features.helpers.zones import Zone6
from src.features.helpers.zones import Zone7
from src.features.helpers.zones import Zone8


class POS():

    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    @property
    def value(self):
        try:
            p = self.event['p']
            self.addMetaArea(self.zone.clockWiseZonePoints,
                             fillColor=self.color)

            return 1 if self.zone.isInZone(p) else 0
        except TypeError:
            return None
        except Exception as e:
            print(e)
            # raise e


class POS8(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone8()
    color = 'cyan'


class POS6(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone6()
    color = 'blue'


class POS5(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone5()
    color = 'cyan'


class POS7(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone7()
    color = 'yellow'


class POS2(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone2()
    color = 'green'


class POS3(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone3()
    color = 'purple'


class POS4(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone4()
    color = 'red'


class POS1(Leaf):
    prototypes = [POS] + POS.prototypes
    zone = Zone1()
    color = 'grey'
