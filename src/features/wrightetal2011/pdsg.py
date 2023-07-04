from contrib.pyas.src.pyas_v3 import Leaf

from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011


class PDSG:

    from src.features.oppgoal.alloppgoalblockercount import AllOppGoalBlockerCount

    prototypes = [AllOppGoalBlockerCount] + AllOppGoalBlockerCount.prototypes \
        + [Wrightetal2011] + Wrightetal2011.prototypes

    @staticmethod
    def featureName(cls):
        name = cls.__name__.split('_')[0:2]
        return '_'.join(name)

    @property
    def value(self):
        blockerCount = super().value
        self.addMetaKeyVal('blockerCount', str(blockerCount))
        res = (self.minPlayers is None or blockerCount >= self.minPlayers) \
            and (self.maxPlayers is None or blockerCount <= self.maxPlayers)
        return 1 if res is True else 0


class PDSG0_2(Leaf):
    prototypes = [PDSG] + PDSG.prototypes
    minPlayers = 0
    maxPlayers = 2


class PDSG3_5(Leaf):
    prototypes = [PDSG] + PDSG.prototypes
    minPlayers = 3
    maxPlayers = 5


class PDSG6_8(Leaf):
    prototypes = [PDSG] + PDSG.prototypes
    minPlayers = 6
    maxPlayers = 8


class PDSGAtLeast9(Leaf):
    prototypes = [PDSG] + PDSG.prototypes
    minPlayers = 9
    maxPlayers = None
