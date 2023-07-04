from statsmodels.discrete import discrete_model as dm

from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.plotters.statsmodelsplotter import StatsModelsPlotter


class StatsModelsLogitPlotter(Leaf):

    prototypes = [StatsModelsPlotter] + StatsModelsPlotter.prototypes

    columnSpecs = {
        'statsResultsClass': {
            'transformer': lambda val, key, classee: dm.LogitResults,
        },
    }
