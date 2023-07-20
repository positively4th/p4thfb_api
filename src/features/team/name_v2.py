from contrib.pyas.src.pyas_v3 import Leaf

from src.features.team.team_v2 import Team
from features.team.name import Name as Name0


class Name(Leaf):

    prototypes = [
        Name0, *Name0.prototypes,
        Team, *Team.prototypes,
    ]

    @property
    async def value(self):
        return self._value()
