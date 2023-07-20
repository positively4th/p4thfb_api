from collections import OrderedDict
import numpy as np
from scipy.stats import norm
import ramda as R

from contrib.pyas.src.pyas_v3 import As

from src.player import Player
from src.constants.pitch import Pitch as P
from src.tools.linalg import LinAlg

pitchTgoalCenter = [
    [-1, 0, P.ext[0] - 0.5 * P.ext[0]],
    [0, -1, 120],
    [0, 0, 1],
]

cdf = norm(0, 1).cdf


def hitProbability(d, r):
    return np.exp(-d)
    # return cdf(d+r) \
    #    - cdf(d-r)


class Block:

    prototypes = []

    pitchTgoalCenter = pitchTgoalCenter
    goalCenterTpitch = np.linalg.inv(pitchTgoalCenter)

    goalSampleSize = 3
    gWidth = 7.32
    ballRadius = 0.221 / 2

    @classmethod
    def onNew(cls, self):
        self.hitProbability = lambda d: hitProbability(d, Block.ballRadius)
        self.playerFilters = []

    def _value(self, players):
        def playerIntersection(gSample, gBall, gPlayer):
            a = gSample
            n = np.subtract(gBall, gSample)
            t = np.linalg.norm(n)
            n = np.multiply(1.0 / t, n)
            p = gPlayer
            d = np.subtract(p, a)
            dist = np.dot(d, n)
            hit = np.add(a, np.multiply(dist, n))
            return hit, dist / t

        eventee = self.eventee
        gBall = LinAlg.transform(eventee.p, P.sbpTpitch, self.pitchTgoalCenter)
        # self.addMetaAnnotation(gBall, 'B', Ts=[self.goalCenterTpitch, P.pitchTsbp])
        pWeigted = 0

        playerPsMap = OrderedDict({})

        for gSample in self.goalSamples:
            p = 1.0
            for sbpPlayer in players:
                playeree = As(Player)(sbpPlayer)
                gPlayer = LinAlg.transform(
                    playeree.p, P.sbpTpitch, self.pitchTgoalCenter)

                gHit, relDist = playerIntersection(gSample, gBall, gPlayer)
                if relDist < 0 or relDist > 1:
                    continue

                if not playeree['__id'] in playerPsMap:
                    playerPsMap[playeree['__id']] = []
                    self.addMetaAnnotation(gPlayer, str(len(playerPsMap)), Ts=[
                                           self.goalCenterTpitch, P.pitchTsbp])

                # self.addMetaArrow(gSample, np.subtract(gPlayer, gSample), Ts=[self.goalCenterTpitch, P.pitchTsbp])
                hitDistance = np.linalg.norm(np.subtract(gHit, gPlayer))
                pHit = self.hitProbability(hitDistance)

                playerPsMap[playeree['__id']].append((gSample[0], pHit))
                if pHit >= 0.005:
                    self.addMetaArrow(gBall, np.subtract(gSample, gBall), Ts=[
                                      self.goalCenterTpitch, P.pitchTsbp])
                    self.addMetaArrow(gPlayer, np.subtract(gHit, gPlayer), Ts=[
                                      self.goalCenterTpitch, P.pitchTsbp])
                p *= (1.0 - pHit)

            pWeigted += p / float(len(self.goalSamples))

        for ix, __id in enumerate(playerPsMap.keys()):
            key = 'P Block #{}'.format(ix+1)
            val = R.pipe(
                R.map(
                    lambda xp: '{}={}%'.format(
                        round(xp[0], 1), int(round(100 * xp[1], 0)))
                ),
                lambda texts: ', '.join(texts)
            )(playerPsMap[__id])

            self.addMetaKeyVal(key, val)

        return 1.0 - pWeigted

    @property
    def value(self):
        raise Exception('Not implemented')

    @property
    def goalSamples(self):
        outer = np.linspace(-0.5 * self.gWidth, 0.5 *
                            self.gWidth, self.goalSampleSize+1)
        return [
            [0.5 * (outer[i] + outer[i+1]), 0, 1] for i in range(0, self.goalSampleSize)
        ]
