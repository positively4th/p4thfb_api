from contrib.pyas.src.pyas_v3 import Leaf

from src.features.player.player_v1 import Player
from features.player.name import Name as Name0


class Name(Leaf):

    prototypes = [
        Name0, *Name0.prototypes,
        Player, *Player.prototypes,
    ]

    @property
    def value(self):
        return self._value()
