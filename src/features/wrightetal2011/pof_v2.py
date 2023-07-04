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
from src.features.wrightetal2011.feed_v2 import Feed


class POF:
    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    @property
    async def value(self):
        try:
            if self.zone is not None:
                self.addMetaArea(self.zone.clockWiseZonePoints,
                                 fillColor=self.color)

            feedee = As(Feed)(self.event)
            pofEvent, rofEvent, error = await feedee.fromToPair
            if error:
                self.addMetaKeyVal('Error', error)
            if rofEvent:
                pROF = As(Event)(rofEvent).p
                self.addMetaAnnotation(pROF, 'rof')
            if pofEvent:
                pPOF = As(Event)(pofEvent).p
                self.addMetaAnnotation(pPOF, 'pof')
            if rofEvent and pofEvent:
                self.addMetaArrow(pPOF, np.subtract(pROF, pPOF))

            if rofEvent is None or pofEvent is None:
                return 1 if self.zone is None else None

            return 1 if (self.zone is not None and self.zone.isInZone(pPOF)) else 0

        except TypeError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            raise e


class POF8(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone8()
    color = 'cyan'


class POF6(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone6()
    color = 'blue'


class POF5(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone5()
    color = 'cyan'


class POF7(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone7()
    color = 'yellow'


class POF2(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone2()
    color = 'green'


class POF3(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone3()
    color = 'purple'


class POF4(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone4()
    color = 'red'


class POF1(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = Zone1()
    color = 'grey'


class NOPOF(Leaf):
    prototypes = [POF] + POF.prototypes
    zone = None
    color = None
