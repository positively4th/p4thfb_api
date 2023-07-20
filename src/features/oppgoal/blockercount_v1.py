
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.player import Player
from src.features.feature_v1 import Feature
from src.features.oppgoal.blockercount import BlockerCount as BlockerCount0


class BlockerCount(Leaf):

    prototypes = [BlockerCount0] + BlockerCount0.prototypes + \
        [Feature] + Feature.prototypes

    @property
    def value(self):

        players = As(Player).pipe(
            self.eventee['visiblePlayers'], self.playerFilters)

        return self._value(players)
