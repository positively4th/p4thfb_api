
from contrib.pyas.src.pyas_v3 import Leaf
from src.features.feature_v2 import Feature
from src.features.isheader import IsHeader as IsHeader0


class IsHeader(Leaf):

    prototypes = [
        IsHeader0, *IsHeader0.prototypes,
        Feature, *Feature.prototypes,
    ]

    def __init__(self, event, *args, **kwargs):
        super().__init__(event, *args, **kwargs)

    @property
    async def value(self):
        eventee = self.eventee
        ttype = await eventee['type']
        return self._value(ttype)
