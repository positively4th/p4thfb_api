from statsmodels.discrete import discrete_model as dm

from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.predictors.statsmodelspredictor import StatsModelsPredictor


class StatsModelsLogitPredictor(Leaf):

    prototypes = [StatsModelsPredictor] + StatsModelsPredictor.prototypes

    columnSpecs = {
        'statsResultsClass': {
            'transformer': lambda val, key, classee: dm.LogitResults,
        },
    }
