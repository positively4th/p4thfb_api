from contrib.pyas.src.pyas_v3 import As
import numpy as np

from src.player import Player
from src.tools.linalg import LinAlg
from src.constants.statsbombpitch import StatsBombPitch as SBP


class BlockerCount:

    prototypes = []

    playerFilters = []

    def _value(self, players):
        eventee = self.eventee

        s = eventee.p
        da = np.subtract(list(SBP.sbLeftOppGoalPost) + [1], s)
        db = np.subtract(list(SBP.sbRightOppGoalPost) + [1], s)

        self.addMetaArrow(s, da)
        self.addMetaArrow(s, db)
        res = 0
        for sbpPlayer in players:
            playeree = As(Player)(sbpPlayer)
            p = playeree.p
            if LinAlg.isInInteriorAngleArea(p, s, da, db):
                res += 1
                self.addMetaAnnotation(p, '1')
        return res

    @property
    async def value(self):
        raise Exception('Not implemented.')
