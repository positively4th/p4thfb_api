from contrib.pyas.src.pyas_v3 import Leaf

from src.features.team.team_v2 import Team


class PossessionName(Leaf):

    prototypes = [Team] + Team.prototypes

    @property
    async def value(self):
        return self.eventee['possessionTeamName']
