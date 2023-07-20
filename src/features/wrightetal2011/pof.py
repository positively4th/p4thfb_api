import numpy as np

from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011


class POF:
    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    def _value(self, pofEventee, rofEventee, error):
        try:
            if self.zone is not None:
                self.addMetaArea(self.zone.clockWiseZonePoints,
                                 fillColor=self.color)

            if error:
                self.addMetaKeyVal('Error', error)
            if rofEventee:
                pROF = rofEventee.p
                self.addMetaAnnotation(pROF, 'rof')
            if pofEventee:
                pPOF = pofEventee.p
                self.addMetaAnnotation(pPOF, 'pof')
            if rofEventee and pofEventee:
                self.addMetaArrow(pPOF, np.subtract(pROF, pPOF))

            if rofEventee is None or pofEventee is None:
                return 1 if self.zone is None else None

            return 1 if (self.zone is not None and self.zone.isInZone(pPOF)) else 0

        except TypeError as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            raise e

    @property
    def value(self):
        raise Exception('Not implemented')
