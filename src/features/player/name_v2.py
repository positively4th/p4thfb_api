from contrib.pyas.src.pyas_v3 import Leaf

from src.features.player.player_v2 import Player


class Name(Leaf):

    prototypes = [Player] + Player.prototypes

    @staticmethod
    def name(cls):
        return 'Player Name'

    @property
    async def value(self):
        return self.eventee['playerName']
