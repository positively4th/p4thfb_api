from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v2 import Feature
from features.outcome.goal import OutcomeGoal as OutcomeGoal0


class OutcomeGoal(Leaf):

    prototypes = [
        OutcomeGoal0, *OutcomeGoal0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    async def value(self):
        return self._value(await self.eventee.outcomeId)
