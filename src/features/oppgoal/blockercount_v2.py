from contrib.pyas.src.pyas_v3 import As
import numpy as np

from player import Player
from src.features.feature_v2 import Feature
from src.tools.linalg import LinAlg
from contrib.pyas.src.pyas_v3 import Leaf

from constants.statsbombpitch import StatsBombPitch as SBP


class BlockerCount(Leaf):

    prototypes = [Feature]

    playerFilters = []

    @property
    async def value(self):

        eventee = self.eventee
        players = As(Player).pipe(
            await eventee['visiblePlayers'], self.playerFilters)

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
