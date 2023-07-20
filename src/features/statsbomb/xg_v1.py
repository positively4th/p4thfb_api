from src.features.feature_v1 import Feature
from src.features.statsbomb.xg import StatsBombXG as StatsBombXG0


class StatsBombXG:

    prototypes = [
        StatsBombXG0, *StatsBombXG0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    def value(self):
        return self._value(self.eventee['type'])
