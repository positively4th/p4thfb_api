from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v2 import Feature

goalOutcomeId = '97'


class OutcomeGoal(Leaf):

    prototypes = [Feature]

    @property
    async def value(self):
        return int((await self.eventee.outcomeId) == goalOutcomeId)
