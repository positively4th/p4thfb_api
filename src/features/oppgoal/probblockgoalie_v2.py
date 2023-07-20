from contrib.pyas.src.pyas_v3 import Leaf

from src.features.oppgoal.block_v2 import Block
from src.features.oppgoal.probblockgoalie import ProbBlockGoalie as ProbBlockGoalie0


class ProbBlockGoalie(Leaf):

    prototypes = [ProbBlockGoalie0] + \
        ProbBlockGoalie0.prototypes + [Block] + Block.prototypes
