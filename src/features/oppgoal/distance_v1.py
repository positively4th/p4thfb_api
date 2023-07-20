
from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v1 import Feature
from features.oppgoal.distance import Distance as Distance0


class Distance(Leaf):

    prototypes = [Distance0] + Distance0.prototypes + \
        [Feature] + Feature.prototypes

    @property
    def value(self):
        return self._value()
