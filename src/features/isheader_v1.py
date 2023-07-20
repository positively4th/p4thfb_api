from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v1 import Feature
from src.features.isheader import IsHeader as IsHeader0


class IsHeader(Leaf):

    prototypes = [
        IsHeader0, *IsHeader0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    def value(self):
        eventee = self.eventee
        ttype = eventee['type']
        return self._value(ttype)
