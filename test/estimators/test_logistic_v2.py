import unittest
import datetime
import numpy as np
from numpy import testing as npt
from scipy.stats import norm
from scipy.special import expit

from contrib.pyas.src.pyas_v3 import As

from src.estimators.logistic_v2 import Logistic
from src.features.feature_v2 import Feature
from src.estimators.mixins.prediction import Prediction
from src.estimators.mixins.estimationnode import EstimationNode
from src.estimators.mixins.estimation import Estimation
from test.estimators.testtools_v2 import createXYTestFeature
from test.estimators.testtools_v2 import XYTestEvent


class TestLogistic_v2(unittest.IsolatedAsyncioTestCase):

    def _generateData(self, N, B):

        rng = np.random.default_rng()

        X = [[1.0] * N]
        X += [
            norm.rvs(1, 1, size=N) for i in range(B.shape[1])
        ]
        X = np.transpose(X)

        p = expit(np.matmul(X, B))
        Y = np.vectorize(lambda _p: rng.binomial(1, _p))(p)
        return Y, X, p

    async def test_1x4(self):
        N = 10000
        beta0 = [
            1,
            -2,
            3,
        ]
        beta1 = np.multiply(-1, beta0)

        beta = np.transpose([
            beta0,
            beta1
        ])

        Y, X, _ = self._generateData(N, beta)
        events = [
            As(XYTestEvent)({
                '__id': i,
                'y': Y[i, :],
                'x': X[i, :],
            }) for i in range(X.shape[0])
        ]

        logistee = As(Logistic)({
            'YFeatureClasses': [
                As(createXYTestFeature('y1', 'y', 0), Feature),
                As(createXYTestFeature('y2', 'y', 1), Feature),
            ],
            'XFeatureClasses': [
                As(createXYTestFeature('x1', 'x', 0), Feature),
                As(createXYTestFeature('x2', 'x', 1), Feature),
                As(createXYTestFeature('x3', 'x', 2), Feature),
            ],
        })

        before = datetime.datetime.now()
        await logistee.estimate(events)
        after = datetime.datetime.now()
        estimations = logistee['estimations']
        self.assertEqual(1, len(estimations))
        estimationee = As(Estimation)(estimations[0])
        self.assertEqual(As(Logistic).estimatorId(), estimationee['id'])
        self.assertEqual(As(Logistic).estimatorNameOrId(),
                         estimationee['name'])
        self.assertLess(before, estimationee['jiff'])
        self.assertGreater(after, estimationee['jiff'])

        estimationNodes = estimationee['estimationNodes']
        assert len(estimationNodes) == 2
        for y in range(len(logistee['YFeatureClasses'])):
            yEstimationNodee = As(EstimationNode)(estimationNodes[y])
            self.assertEqual(Feature.featureId(
                logistee['YFeatureClasses'][y]), yEstimationNodee['id'])
            self.assertEqual(Feature.featureName(
                logistee['YFeatureClasses'][y]), yEstimationNodee['name'])
            self.assertEqual(len(logistee['XFeatureClasses']), len(
                yEstimationNodee['estimationNodes']))
            for x in range(len(logistee['XFeatureClasses'])):
                xEstimationNodee = As(EstimationNode)(
                    yEstimationNodee['estimationNodes'][x])
                self.assertEqual(Feature.featureId(
                    logistee['XFeatureClasses'][x]), xEstimationNodee['id'])
                self.assertEqual(Feature.featureName(
                    logistee['XFeatureClasses'][x]), xEstimationNodee['name'])
                npt.assert_almost_equal(
                    beta[x][y], xEstimationNodee['estimate'], decimal=1)

        betaHat = np.transpose(As(EstimationNode)(
            logistee['estimations'][0]).collectLeaves())
        _, X, exp = self._generateData(20, betaHat)
        events = [As(XYTestEvent)({'y': Y[i, :], 'x': X[i, :], })
                  for i in range(X.shape[0])]

        prediction = await logistee.predict(events, logistee['estimations'][0])
        predictionee = As(Prediction)(prediction)
        self.assertEqual(estimationee['jiff'], predictionee['jiff'])

        act = np.transpose(predictionee.collectLeaves())
        npt.assert_array_almost_equal(exp, act, decimal=5)


if __name__ == '__main__':

    unittest.main()