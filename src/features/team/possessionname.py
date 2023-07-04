from src.features.team.team import Team
from contrib.pyas.src.pyas_v3 import Leaf


class PossessionName(Leaf):

    prototypes = [Team] + Team.prototypes

    @property
    def value(self):
        return self.eventee['possessionTeamName']
