import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.estimators.mixins.estimationnode import EstimationNode


class PredictorError(Exception):
    pass


class Predictor(Leaf):

    prototypes = []

    columnSpecs = {
        'estimator': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }

    def _predict(self, predictor, X):
        raise PredictorError('Not implemented.')

    def predicter(self, estimationNode, X):
        res = R.omit(['estimationNodes', 'estimate',
                     'results'], estimationNode)

        branches = estimationNode['estimationNodes'] if 'estimationNodes' in estimationNode else [
        ]
        if len(branches) == 0:
            res['predictions'] = As(EstimationNode).Skip

        if 'results' in estimationNode:
            res['prediction'] = self._predict(estimationNode['results'], X)
            res['predictions'] = As(EstimationNode).Skip
        return res
