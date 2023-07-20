import numpy as np

from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011


class SPA:

    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    def _value(self, firstEventee):
        try:

            p = self.event['p']

            pStart = firstEventee.p
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

    @property
    def value(self):
        return Exception('Not implemented')
