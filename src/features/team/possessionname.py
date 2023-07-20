from contrib.pyas.src.pyas_v3 import Leaf


class PossessionName(Leaf):

    prototypes = []

    def _value(self):
        return self.eventee['possessionTeamName']

    @property
    async def value(self):
        raise Exception('Not implemented.')
