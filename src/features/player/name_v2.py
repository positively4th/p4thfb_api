from contrib.pyas.src.pyas_v3 import Leaf

from src.features.player.player_v2 import Player
from features.player.name import Name as Name0


class Name(Leaf):

    prototypes = [
        Name0, *Name0.prototypes,
        Player, *Player.prototypes,
    ]

    @property
    async def value(self):
        return self._value()
