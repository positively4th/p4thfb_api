import numpy as np

from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v2 import Feature
from constants.pitch import Pitch as P
from src.tools.linalg import LinAlg

pitchTgoalCenter = [
    [-1, 0, P.ext[0] - 0.5 * P.ext[0]],
    [0, -1, 120],
    [0, 0, 1],
]


class Distance(Leaf):

    prototypes = [Feature]

    pitchTgoalCenter = pitchTgoalCenter
    goalCenterTpitch = np.linalg.inv(pitchTgoalCenter)

    @property
    async def value(self):

        eventee = self.eventee
        pBall = LinAlg.transform(eventee.p, P.sbpTpitch)
        pGoal = [
            0.5 * (P.inf[0] + P.sup[0]),
            P.sup[1],
            1
        ]

        pDelta = np.subtract(pGoal, pBall)
        self.addMetaArrow(pBall, pDelta, Ts=[P.pitchTsbp])

        return np.linalg.norm(pDelta)
