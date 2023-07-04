from contrib.pyas.src.pyas_v3 import Leaf

from src.features.team.team_v2 import Team


class Name(Leaf):

    prototypes = [Team] + Team.prototypes

    @staticmethod
    def name(cls):
        return 'Team Name'

    @property
    async def value(self):
        return self.eventee['eventTeamName']
