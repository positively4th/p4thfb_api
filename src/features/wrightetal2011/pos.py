from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011


class POS:

    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    def _value(self):
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

    @property
    def value(self):
        raise Exception('Not implemented.')
