from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v2 import Feature


class One(Leaf):

    prototypes = [Feature] + Feature.prototypes

    @property
    async def value(self):
        return 1
