from contrib.pyas.src.pyas_v3 import Leaf

from src.player import Player


class ProbBlockGoalie(Leaf):

    prototypes = []

    @classmethod
    def onNew(cls, self):
        self.playerFilters = [Player.notTeammates,
                              Player.notActors, Player.onlyKeepers]
