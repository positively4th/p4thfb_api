import datetime
import unittest
import numpy as np
from numpy import testing as npt
from scipy.stats import norm
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from src.estimators.ols_v2 import OLS
from src.features.feature_v2 import Feature
from src.estimators.mixins.estimation import Estimation
from src.estimators.mixins.estimationnode import EstimationNode
from src.estimators.mixins.prediction import Prediction
from test.estimators.testtools_v2 import XYTestEvent
from test.estimators.testtools_v2 import createXYTestFeature


def createFeature(name):
    return type(name, (Leaf,), {})


class TestOLS_v2(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def _generateData(cls, N, B, s=1):
        e01 = norm(loc=0, scale=s)

        X = [
            [1.0] * N
        ] + [
            norm.rvs(1, 1, size=N) for i in range(B.shape[1])
        ]

        X = np.transpose(X)

        E = e01.rvs(size=(N, 2))
        Y = np.add(np.matmul(X, B), E)
        return Y, X, E

    async def test_1x3(self):
        N = 1000

        beta0 = [
            0.5,
            -1,
            2,
        ]
        beta1 = np.multiply(-1, beta0)

        beta = np.transpose([
            beta0,
            beta1
        ])

        Y, X, _ = self._generateData(N, beta, 1)

        events = [
            As(XYTestEvent)({
                '__id': i,
                'y': Y[i, :],
                'x': X[i, :],
            }) for i in range(X.shape[0])
        ]

        olsee = As(OLS)({
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
        await olsee.estimate(events)
        after = datetime.datetime.now()
        estimations = olsee['estimations']
        self.assertEqual(1, len(estimations))
        estimationee = As(Estimation)(estimations[0])
        self.assertEqual(As(OLS).estimatorId(), estimationee['id'])
        self.assertEqual(As(OLS).estimatorNameOrId(), estimationee['name'])
        self.assertLess(before, estimationee['jiff'])
        self.assertGreater(after, estimationee['jiff'])

        estimationNodes = estimationee['estimationNodes']
        assert len(estimationNodes) == 2
        for y in range(len(olsee['YFeatureClasses'])):
            yEstimationNodee = As(EstimationNode)(estimationNodes[y])
            self.assertEqual(As(Feature).featureId(
                olsee['YFeatureClasses'][y]), yEstimationNodee['id'])
            self.assertEqual(As(Feature).featureName(
                olsee['YFeatureClasses'][y]), yEstimationNodee['name'])
            self.assertEqual(len(olsee['XFeatureClasses']), len(
                yEstimationNodee['estimationNodes']))
            for x in range(len(olsee['XFeatureClasses'])):
                xEstimationNodee = As(EstimationNode)(
                    yEstimationNodee['estimationNodes'][x])
                self.assertEqual(As(Feature).featureId(
                    olsee['XFeatureClasses'][x]), xEstimationNodee['id'])
                self.assertEqual(As(Feature).featureName(
                    olsee['XFeatureClasses'][x]), xEstimationNodee['name'])
                npt.assert_almost_equal(
                    beta[x][y], xEstimationNodee['estimate'], decimal=1)

        prediction = await olsee.predict(events, olsee['estimations'][0])
        predictionee = As(Prediction)(prediction)
        self.assertEqual(estimationee['jiff'], predictionee['jiff'])

        betaHat = np.transpose(As(EstimationNode)(
            olsee['estimations'][0]).collectLeaves())
        exp = np.matmul(X, betaHat)
        act = np.transpose(predictionee.collectLeaves())
        npt.assert_array_almost_equal(exp, act, decimal=5)

    async def testAverage(self):
        from src.features.statsbomb.xg_v2 import StatsBombXG
        from src.features.one_v2 import One
        from src.mappers.event.constants import Constants

        events = [
            {
                '__id': 10,
                'eventId': 10,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 'aa'
                }
            },
            {
                '__id': 20,
                'eventId': 20,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 0.25
                }
            },
            {
                '__id': 30,
                'eventId': 30,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 0.50
                }
            },
            {
                '__id': 40,
                'eventId': 40,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 'bb'
                }
            },
            {
                '__id': 50,
                'eventId': 50,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 0.75
                }
            },
            {
                '__id': 60,
                'eventId': 60,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 'cc'
                }
            },
        ]

        averagee = As(OLS)({
            'YFeatureClasses': [As(StatsBombXG), As(One)],
            'XFeatureClasses': [As(One)]
        })
        before = datetime.datetime.now()
        await averagee.estimate(events)
        after = datetime.datetime.now()
        estimations = averagee['estimations']
        self.assertEqual(1, len(estimations))
        estimationee = As(Estimation)(estimations[0])
        self.assertEqual(As(OLS).estimatorId(), estimationee['id'])
        self.assertEqual(As(OLS).estimatorNameOrId(), estimationee['name'])
        self.assertLess(before, estimationee['jiff'])
        self.assertGreater(after, estimationee['jiff'])

        estimationNodes = estimationee['estimationNodes']
        assert len(estimationNodes) == 2

        for y in range(len(averagee['YFeatureClasses'])):
            yEstimationNodee = As(EstimationNode)(estimationNodes[y])
            self.assertEqual(As(Feature).featureId(
                averagee['YFeatureClasses'][y]), yEstimationNodee['id'])
            self.assertEqual(As(Feature).featureName(
                averagee['YFeatureClasses'][y]), yEstimationNodee['name'])
            self.assertEqual(len(averagee['XFeatureClasses']), len(
                yEstimationNodee['estimationNodes']))
            for x in range(len(averagee['XFeatureClasses'])):
                xEstimationNodee = As(EstimationNode)(
                    yEstimationNodee['estimationNodes'][x])
                self.assertEqual(As(Feature).featureId(
                    averagee['XFeatureClasses'][x]), xEstimationNodee['id'])
                self.assertEqual(As(Feature).featureName(
                    averagee['XFeatureClasses'][x]), xEstimationNodee['name'])
                assert xEstimationNodee['estimate'] == (y + 1) * 0.5

        prediction = await averagee.predict(events, averagee['estimations'][0])
        predictionee = As(Prediction)(prediction)
        self.assertEqual(estimationee['jiff'], predictionee['jiff'])

        act = np.transpose(predictionee.collectLeaves())
        exp = np.transpose([
            [0.5] * len(events),
            [1.0] * len(events)
        ])
        npt.assert_array_almost_equal(exp, act, decimal=5)


if __name__ == '__main__':

    unittest.main()
