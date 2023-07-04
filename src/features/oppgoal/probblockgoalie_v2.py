from contrib.pyas.src.pyas_v3 import Leaf

from src.player import Player
from src.features.oppgoal.block_v2 import Block


class ProbBlockGoalie(Leaf):

    prototypes = [Block] + Block.prototypes

    @classmethod
    def onNew(cls, self):
        self.playerFilters = [Player.notTeammates,
                              Player.notActors, Player.onlyKeepers]
