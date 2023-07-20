from contrib.pyas.src.pyas_v3 import As

from src.player import Player
from src.features.feature_v2 import Feature
from src.features.oppgoal.block import Block as Block0


class Block:

    prototypes = [Block0] + Block0.prototypes + [Feature] + Feature.prototypes

    @property
    async def value(self):

        players = As(Player).pipe(
            await self.eventee['visiblePlayers'], self.playerFilters)

        return self._value(players)
