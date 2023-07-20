from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v1 import Feature
from src.features.feature_v1 import Feature
from features.oppgoal.width import Width as Width0


class Width(Leaf):

    prototypes = [Width0] + Width0.prototypes + [Feature] + Feature.prototypes

    @property
    def value(self):
        return self._value()
