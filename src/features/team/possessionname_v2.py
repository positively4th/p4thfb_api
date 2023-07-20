from contrib.pyas.src.pyas_v3 import Leaf

from src.features.team.team_v2 import Team
from features.team.possessionname import PossessionName as PossessionName0


class PossessionName(Leaf):

    prototypes = [
        PossessionName0, *PossessionName0.prototypes,
        Team, *Team.prototypes,
    ]

    @property
    async def value(self):
        return self._value()
