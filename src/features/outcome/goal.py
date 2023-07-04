from src.features.feature import Feature
from contrib.pyas.src.pyas_v3 import Leaf

goalOutcomeId = '97'


class OutcomeGoal(Leaf):

    prototypes = [Feature]

    @property
    def value(self):
        return int(self.eventee.outcomeId == goalOutcomeId)
