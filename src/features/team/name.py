from src.features.team.team import Team
from contrib.pyas.src.pyas_v3 import Leaf


class Name(Leaf):

    prototypes = [Team] + Team.prototypes

    @staticmethod
    def name(cls):
        return 'Team Name'

    @property
    def value(self):
        return self.eventee['eventTeamName']
