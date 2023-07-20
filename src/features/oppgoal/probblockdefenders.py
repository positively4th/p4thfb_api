from src.player import Player


class ProbBlockDefenders:

    prototypes = []

    @classmethod
    def onNew(cls, self):
        self.playerFilters = [Player.notTeammates,
                              Player.notActors, Player.notKeepers]
