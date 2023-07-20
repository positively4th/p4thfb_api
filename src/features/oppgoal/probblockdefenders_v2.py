from contrib.pyas.src.pyas_v3 import Leaf

from src.features.oppgoal.block_v2 import Block
from src.features.oppgoal.probblockdefenders import ProbBlockDefenders as ProbBlockDefenders0


class ProbBlockDefenders(Leaf):

    prototypes = [
        ProbBlockDefenders0, *ProbBlockDefenders0.prototypes,
        Block, *Block.prototypes
    ]
