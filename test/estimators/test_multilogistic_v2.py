import unittest
import numpy as np
from numpy import testing as npt
import datetime
from scipy.stats import norm
from src.estimators.multilogistic_v2 import MultiLogistic
from contrib.pyas.src.pyas_v3 import As
from src.features.feature_v2 import Feature
from src.estimators.mixins.estimation import Estimation
from src.estimators.mixins.estimationnode import EstimationNode
from src.estimators.mixins.prediction import Prediction

from test.estimators.testtools_v2 import XYTestEvent
from test.estimators.testtools_v2 import createXYTestFeature


class TestMultiLogistic_v2(unittest.IsolatedAsyncioTestCase):

    # https://github.com/statsmodels/statsmodels/issues/837
    # Choice of ref category is first after sorting alphabetically

    def _generateOne(self, N, Bs, X=None):

        rng = np.random.default_rng()

        def Pk(k, zs, z):
            return zs[:, k] / (1 + z)

        def cat(Pks):
            u = rng.uniform()
            for i, P in enumerate(Pks):
                if u < P:
                    return 'Cat_' + str(i)
                u -= P

            assert 1 == 0, 'Invalid probability'

        if X is None:
            X = [[1.0] * N]
            X += [
                norm.rvs(1, 1, size=N) for i in range(Bs.shape[1])
            ]
            X = np.transpose(X)

        zs = np.exp(np.matmul(X, Bs))
        z = np.sum(zs[:, 1:], axis=1)

        Pks = [Pk(k, zs, z) for k in range(Bs.shape[1])]
        Pks = np.transpose(Pks)
        Y = np.transpose([
            cat(Pks[i]) for i in range(N)
        ])
        return Y, X, Pks

    async def test_binary(self):
        N = 10000
        beta00 = [0, 0, 0,]
        beta01 = [1, -2, 3]
        betas = np.transpose([beta00, beta01])

        Y, X, _ = self._generateOne(N, betas)
        events = [
            As(XYTestEvent)({
                '__id': i,
                'eventId': i,
                'y': [Y[i]],
                'x': X[i, :],
            }) for i in range(X.shape[0])
        ]

        mlee = As(MultiLogistic)({
            'YFeatureClasses': [
                As(createXYTestFeature('y1', 'y', 0), Feature),
            ],
            'XFeatureClasses': [
                As(createXYTestFeature('x1', 'x', 0), Feature),
                As(createXYTestFeature('x2', 'x', 1), Feature),
                As(createXYTestFeature('x3', 'x', 2), Feature),
            ],
        })

        before = datetime.datetime.now()
        await mlee.estimate(events)
        after = datetime.datetime.now()
        estimations = mlee['estimations']
        self.assertEqual(1, len(estimations))
        estimationee = As(Estimation)(estimations[0])
        self.assertEqual(As(MultiLogistic).estimatorId(), estimationee['id'])
        self.assertEqual(As(MultiLogistic).estimatorNameOrId(),
                         estimationee['name'])
        self.assertLess(before, estimationee['jiff'])
        self.assertGreater(after, estimationee['jiff'])

        estimationNodes = estimationee['estimationNodes']
        assert len(estimationNodes) == 1
        for y in range(len(mlee['YFeatureClasses'])):
            yEstimationNodee = As(EstimationNode)(estimationNodes[y])
            self.assertEqual(As(Feature).featureId(
                mlee['YFeatureClasses'][y]), yEstimationNodee['id'])
            self.assertEqual(As(Feature).featureName(
                mlee['YFeatureClasses'][y]), yEstimationNodee['name'])
            categories = yEstimationNodee['categories']
            self.assertEqual(len(categories), len(
                yEstimationNodee['estimationNodes']))
            for c in range(len(categories)):
                cEstimationNodee = As(EstimationNode)(
                    yEstimationNodee['estimationNodes'][c])
                self.assertEqual(categories[c], cEstimationNodee['name'])
                self.assertEqual(len(mlee['XFeatureClasses']), len(
                    cEstimationNodee['estimationNodes']))
                for x in range(len(mlee['XFeatureClasses'])):
                    xEstimationNodee = As(EstimationNode)(
                        cEstimationNodee['estimationNodes'][x])
                    self.assertEqual('{}:{}'.format(categories[c], As(Feature).featureId(mlee['XFeatureClasses'][x])),
                                     xEstimationNodee['id'])
                    self.assertEqual(As(Feature).featureName(
                        mlee['XFeatureClasses'][x]), xEstimationNodee['name'])
                    # Only 1 y to estimate,skip y-index.
                    npt.assert_almost_equal(
                        betas[x][c], xEstimationNodee['estimate'], decimal=1)

        betaHat = As(EstimationNode)(mlee['estimations'][0]).collectLeaves()
        betaHat = np.transpose(betaHat[0])
        Y, X, exp = self._generateOne(10, betaHat)
        events = [
            As(XYTestEvent)({
                'y': [Y[i]],
                'x': X[i, :],
            }) for i in range(X.shape[0])
        ]

        prediction = await mlee.predict(events, mlee['estimations'][0])
        predictionee = As(Prediction)(prediction)
        self.assertEqual(estimationee['jiff'], predictionee['jiff'])

        act = np.transpose(predictionee.collectLeaves()[0])
        npt.assert_array_almost_equal(exp, act, decimal=5)


if __name__ == '__main__':

    unittest.main()
