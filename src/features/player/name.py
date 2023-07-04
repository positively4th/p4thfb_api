from contrib.pyas.src.pyas_v3 import Leaf

from src.features.player.player import Player


class Name(Leaf):

    prototypes = [Player] + Player.prototypes

    @staticmethod
    def name(cls):
        return 'Player Name'

    @property
    def value(self):
        return self.eventee['playerName']
