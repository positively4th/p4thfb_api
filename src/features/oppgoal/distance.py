import numpy as np

from constants.pitch import Pitch as P
from src.tools.linalg import LinAlg

pitchTgoalCenter = [
    [-1, 0, P.ext[0] - 0.5 * P.ext[0]],
    [0, -1, 120],
    [0, 0, 1],
]


class Distance:

    prototypes = []

    pitchTgoalCenter = pitchTgoalCenter
    goalCenterTpitch = np.linalg.inv(pitchTgoalCenter)

    def _value(self):
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

    @property
    async def value(self):
        raise Exception('Not implemented')
