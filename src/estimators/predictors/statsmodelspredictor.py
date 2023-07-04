import io
import base64
from statsmodels.discrete.discrete_model import MultinomialResultsWrapper

from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.predictors.predictor import Predictor
from src.tools.numpy import Numpy as NP


class StatsModelsPredictor(Leaf):

    prototypes = [Predictor] + Predictor.prototypes

    columnSpecs = {
        'statsResultsClass': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }

    def deserializeResults(self, serialized):
        serializedResults = io.BytesIO(base64.decodebytes(serialized))
        res = self['statsResultsClass'].load(serializedResults)
        return res

    def _predict(self, results, X):

        def predictLogistic(r, X):
            return r.predict(X)

        def predictLinear(r, X):
            return r.get_prediction(X).predicted

        results = self.deserializeResults(results)

        if isinstance(results, MultinomialResultsWrapper):
            return predictLogistic(results, NP.asArray(X))
        if hasattr(results, 'get_prediction'):
            return predictLinear(results, NP.asArray(X))
        elif hasattr(results, 'predict'):
            return predictLogistic(results, NP.asArray(X))
