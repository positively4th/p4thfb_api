from contrib.pyas.src.pyas_v3 import Leaf

from src.player import Player


class AllOppGoalBlockerCount(Leaf):

    from src.features.oppgoal.blockercount import BlockerCount

    prototypes = [BlockerCount] + BlockerCount.prototypes

    playerFilters = [Player.notActors]
