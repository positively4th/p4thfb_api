import numpy as np

from src.constants.pitch import Pitch as P
from src.tools.linalg import LinAlg

pitchTgoalCenter = [
    [-1, 0, P.ext[0] - 0.5 * P.ext[0]],
    [0, -1, 120],
    [0, 0, 1],
]


class Width:

    prototypes = []

    pitchTgoalCenter = pitchTgoalCenter
    goalCenterTpitch = np.linalg.inv(pitchTgoalCenter)

    goalSampleSize = 3
    gWidth = 7.32
    ballRadius = 0.221 / 2

    def _value(self):
        eventee = self.eventee
        gBall = LinAlg.transform(eventee.p, P.sbpTpitch, self.pitchTgoalCenter)
        width = 0.0
        for gPost in self.goalPosts:
            dGoal2Ball = LinAlg.normalize(np.subtract(gBall, self.goalCenter))
            nGoal2Ball = LinAlg.orthogonal(dGoal2Ball)
            i = LinAlg.rayRayIntersection(gPost, dGoal2Ball, gBall, nGoal2Ball)
            if i is None:
                continue
            distPost, distBall = i
            gCross = np.add(gPost, np.multiply(distPost, dGoal2Ball))

            self.addMetaArrow(gPost, np.subtract(gCross, gPost), Ts=[
                              self.goalCenterTpitch, P.pitchTsbp])
            self.addMetaArrow(gBall, np.subtract(gCross, gBall), Ts=[
                              self.goalCenterTpitch, P.pitchTsbp])

            width = width + np.abs(distBall)
        self.addMetaAnnotation(gBall, str(round(width, 2)), Ts=[
                               self.goalCenterTpitch, P.pitchTsbp])
        return width / self.gWidth

    @property
    def value(self):
        raise Exception('Not implemented')

    @property
    def goalPosts(self):
        outer = np.linspace(-0.5 * self.gWidth, 0.5 * self.gWidth, 2)
        return [
            [x, 0, 1] for x in outer
        ]

    @property
    def goalCenter(self):
        return [0, 0, 1]
