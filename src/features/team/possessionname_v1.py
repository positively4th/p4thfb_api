from contrib.pyas.src.pyas_v3 import Leaf

from features.team.possessionname import PossessionName as PossessionName0
from features.team.team_v1 import Team


class PossessionName(Leaf):

    prototypes = [
        PossessionName0, *PossessionName0.prototypes,
        Team, *Team.prototypes,
    ]

    @property
    def value(self):
        return self._value()
