from src.features.feature import Feature
from contrib.pyas.src.pyas_v3 import Leaf


class StatsBombXG(Leaf):

    prototypes = [Feature] + Feature.prototypes

    @property
    def value(self):
        xG = float(self.eventee.xG)
        return xG \
            if xG == xG and xG != float('inf') and xG != float('-inf') \
            else float('{} is not a valid number.'.format(self.eventee.xG))
