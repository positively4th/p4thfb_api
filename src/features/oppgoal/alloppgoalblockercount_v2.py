from src.player import Player
from contrib.pyas.src.pyas_v3 import Leaf


class AllOppGoalBlockerCount(Leaf):

    from src.features.oppgoal.blockercount_v2 import BlockerCount

    prototypes = [BlockerCount] + BlockerCount.prototypes

    playerFilters = [Player.notActors]
