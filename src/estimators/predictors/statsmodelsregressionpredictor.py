import statsmodels.regression.linear_model as lm

from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.predictors.statsmodelspredictor import StatsModelsPredictor


class StatsModelsRegressionPredictor(Leaf):

    prototypes = [StatsModelsPredictor] + StatsModelsPredictor.prototypes

    columnSpecs = {
        'statsResultsClass': {
            'transformer': lambda val, key, classee: lm.RegressionResults,
        },
    }
