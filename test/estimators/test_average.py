import unittest
import datetime
import numpy as np
import numpy.testing as npt
from src.features.feature import Feature
from src.estimators.average import Average
from contrib.pyas.src.pyas_v3 import As
from src.estimators.mixins.estimationnode import EstimationNode
from src.estimators.mixins.estimation import Estimation
from src.estimators.mixins.prediction import Prediction


class TestAverage(unittest.TestCase):

    def testSimple(self):
        from src.features.statsbomb.xg import StatsBombXG
        from src.features.one import One

        events = [
            {
                '__id': 10,
                'type': {
                    'xG': 'aa'
                }
            },
            {
                '__id': 20,
                'type': {
                    'xG': 0.25
                }
            },
            {
                '__id': 30,
                'type': {
                    'xG': 0.50
                }
            },
            {
                '__id': 40,
                'type': {
                    'xG': 'bb'
                }
            },
            {
                '__id': 50,
                'type': {
                    'xG': 0.75
                }
            },
            {
                '__id': 60,
                'type': {
                    'xG': 'cc'
                }
            },
        ]

        averagee = As(Average)({
            'YFeatureClasses': [As(StatsBombXG), As(One)]
        })

        before = datetime.datetime.now()
        averagee.estimate(events)
        after = datetime.datetime.now()
        estimations = averagee['estimations']
        self.assertEqual(1, len(estimations))
        estimationee = As(Estimation)(estimations[0])
        self.assertEqual(As(Average).estimatorId(), estimationee['id'])
        self.assertEqual(As(Average).estimatorNameOrId(), estimationee['name'])
        self.assertLess(before, estimationee['jiff'])
        self.assertGreater(after, estimationee['jiff'])

        estimationNodes = estimationee['estimationNodes']
        assert len(estimationNodes) == 2

        for y in range(len(averagee['YFeatureClasses'])):
            yEstimationNodee = As(EstimationNode)(estimationNodes[y])
            self.assertEqual(Feature.featureId(
                averagee['YFeatureClasses'][y]), yEstimationNodee['id'])
            self.assertEqual(Feature.featureName(
                averagee['YFeatureClasses'][y]), yEstimationNodee['name'])
            self.assertEqual(1, len(yEstimationNodee['estimationNodes']))
            for x in range(1):
                xEstimationNodee = As(EstimationNode)(
                    yEstimationNodee['estimationNodes'][x])
                self.assertEqual('1', xEstimationNodee['id'])
                self.assertEqual('Mean', xEstimationNodee['name'])
                assert xEstimationNodee['estimate'] == (y + 1) * 0.5

        prediction = averagee.predict(events, averagee['estimations'][0])
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
