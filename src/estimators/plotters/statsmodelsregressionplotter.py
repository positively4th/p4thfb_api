import statsmodels.regression.linear_model as lm

from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.plotters.statsmodelsplotter import StatsModelsPlotter


class StatsModelsRegressionPlotter(Leaf):

    prototypes = [StatsModelsPlotter] + StatsModelsPlotter.prototypes

    columnSpecs = {
        'statsResultsClass': {
            'transformer': lambda val, key, classee: lm.RegressionResults,
        },
    }
