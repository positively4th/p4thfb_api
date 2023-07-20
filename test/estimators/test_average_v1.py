import unittest
import datetime
import numpy as np
import numpy.testing as npt

from contrib.pyas.src.pyas_v3 import As

from src.features.feature_v1 import Feature
from src.estimators.average_v1 import Average
from src.mappers.event.constants import Constants
from src.estimators.mixins.estimationnode import EstimationNode
from src.estimators.mixins.estimation import Estimation
from src.estimators.mixins.prediction import Prediction
from src.features.statsbomb.xg_v1 import StatsBombXG
from src.features.one_v1 import One


class TestAverage(unittest.TestCase):

    def testSimple(self):

        events = [
            {
                '__id': 10,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 'aa'
                }
            },
            {
                '__id': 20,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 0.25
                }
            },
            {
                '__id': 30,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 0.50
                }
            },
            {
                '__id': 40,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 'bb'
                }
            },
            {
                '__id': 50,
                'typeId': Constants.shotTypeId,
                'type': {
                    'xG': 0.75
                }
            },
            {
                '__id': 60,
                'typeId': Constants.shotTypeId,
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
            self.assertEqual(As(Feature).featureId(
                averagee['YFeatureClasses'][y]), yEstimationNodee['id'])
            self.assertEqual(As(Feature).featureName(
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
