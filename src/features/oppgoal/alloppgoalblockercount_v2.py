from contrib.pyas.src.pyas_v3 import Leaf

from src.features.oppgoal.blockercount_v2 import BlockerCount
from features.oppgoal.alloppgoalblockercount import AllOppGoalBlockerCount as AllOppGoalBlockerCount0


class AllOppGoalBlockerCount(Leaf):

    prototypes = [AllOppGoalBlockerCount0] + \
        AllOppGoalBlockerCount0.prototypes + \
        [BlockerCount] + BlockerCount.prototypes
