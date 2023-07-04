import numpy as np

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from player import Player
from src.features.feature import Feature
from src.tools.linalg import LinAlg
from constants.statsbombpitch import StatsBombPitch as SBP


class BlockerCount(Leaf):

    prototypes = [Feature] + Feature.prototypes

    playerFilters = []

    @property
    def value(self):

        eventee = self.eventee
        players = As(Player).pipe(
            eventee['visiblePlayers'], self.playerFilters)

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
