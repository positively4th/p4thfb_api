import numpy as np
import ramda as R
from src.features.feature import Feature
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.mixins.classnamed import ClassNamed
from src.mixins.classidentified import ClassIdentified
from src.estimators.estimator import Estimator
from src.estimators.mixins.estimationnode import EstimationNode
from src.tools.numpy import Numpy as NP


class Average(Leaf):

    prototypes = [Estimator] + Estimator.prototypes \
        + [ClassIdentified, ClassNamed] \
        + ClassIdentified.prototypes + ClassNamed.prototypes

    def predicter(self, estimationNode, X):
        res = {
            'id': estimationNode['id'],
            'name': estimationNode['name'],
        }
        if 'jiff' in estimationNode:
            res['jiff'] = estimationNode['jiff']

        branches = estimationNode['estimationNodes'] if 'estimationNodes' in estimationNode else [
        ]
        if len(branches) == 0:
            res['predictionNodes'] = As(EstimationNode).Skip

        noEstimateCount = R.reduce(
            lambda c, e: c - 1 if 'estimate' not in e else 0)(0, branches)

        if 'estimationNodes' in estimationNode and noEstimateCount == 0:
            for e in estimationNode['estimationNodes']:
                res['prediction'] = [e['estimate']] * X.shape[0]
        return res

    def estimater(self, X, Y):

        YFeatureClasses = self['YFeatureClasses']
        estimate = [np.mean(Y[name]) for name in NP.columnNames(Y)]

        estimationNode = [
            {
                'id': Feature.featureId(YFeatureClasses[i]),
                'name': Feature.featureName(YFeatureClasses[i]),
                'estimationNodes': [
                    {
                        'id': '1',
                        'name': 'Mean',
                        'estimate': estimate,
                    }
                ],
                'N': Y.shape[0],
            }
            for i, estimate in enumerate(estimate)
        ]

        return estimationNode
