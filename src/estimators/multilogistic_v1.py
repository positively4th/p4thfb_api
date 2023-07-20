import numpy as np
import ramda as R
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from src.estimators.estimator_v1 import Estimator
from src.estimators.estimaters.statsmodelsmnlogitestimater import StatsModelsMultiNMLogitEstimater
from src.estimators.predictors.statsmodelslogitpredictor import StatsModelsLogitPredictor
from src.estimators.plotters.statsmodelslogitplotter import StatsModelsLogitPlotter
from src.estimators.mixins.predictionnode import PredictionNode


class MultiLogistic:

    prototypes = [StatsModelsLogitPredictor] + StatsModelsLogitPredictor.prototypes \
        + [StatsModelsLogitPlotter] + StatsModelsLogitPlotter.prototypes \
        + [StatsModelsMultiNMLogitEstimater] + StatsModelsMultiNMLogitEstimater.prototypes \
        + [Estimator] + Estimator.prototypes

    columnSpecs = {
        'estimate': {
            'transformer': lambda val, key, classee: val if key in classee.row else [],
        },
    }

    def estimater(self, X, Y):

        def pivotNode(estimationNode):
            cats = estimationNode['categories']
            estimationNode0 = {**estimationNode}
            if 'estimate' in estimationNode0:
                del estimationNode0['estimate']
            estimationNode0['estimationNodes'] = []
            for i, cat in enumerate(cats):
                estimationNodes1 = []
                for estimate1 in estimationNode['estimationNodes']:
                    estimationNodes1.append({
                        **estimate1,
                        **{
                            'id': '{}:{}'.format(cat, estimate1['id']),
                            'name': estimate1['name'],
                            'estimate': estimate1['estimate'][i - 1] if i > 0 else 0
                        }
                    })

                estimationNode0['estimationNodes'].append({
                    'name': cat,
                    'estimationNodes': estimationNodes1,
                })
            return estimationNode0

        estimationNodes = super().estimater(X, Y)
        estimationNodes0 = []
        for i, estimationNode in enumerate(estimationNodes):
            estimationNode['categories'] = sorted(
                np.unique(Y[estimationNode['id']]))
            estimationNodes0.append(pivotNode(estimationNode))

        return estimationNodes0

    def predict(self, events, estimation):

        def splitPredictions(predictionNode):
            res = {
                'id': predictionNode['id'],
                'name': predictionNode['name'],
            }
            if 'jiff' in predictionNode:
                res['jiff'] = predictionNode['jiff']

            if 'prediction' not in predictionNode:
                return res

            prediction = predictionNode['prediction']
            res['predictionNodes'] = res['predictionNodes'] if 'predictionNodes' in res else []
            for i, category in enumerate(predictionNode['categories']):
                p = {
                    **{
                        'id': predictionNode['id'] + ':' + category,
                        'name': category,
                        'prediction': prediction[:, i]
                    }
                }
                res['predictionNodes'].append(R.omit(['predictionNodes'], p))
            return res

        compoundPredictions = super().predict(events, estimation)
        return As(PredictionNode)(compoundPredictions).map(splitPredictions)
