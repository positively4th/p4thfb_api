from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature import Feature


class One(Leaf):

    prototypes = [Feature] + Feature.prototypes

    @property
    def value(self):
        return 1
