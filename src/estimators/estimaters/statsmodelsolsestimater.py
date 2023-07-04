import statsmodels.api as sm

from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.estimaters.statsmodelsestimater import StatsModelsEstimater


class StatsModelsOLSEstimater(Leaf):

    prototypes = [StatsModelsEstimater] + StatsModelsEstimater.prototypes

    columnSpecs = {
        'statsModel': {
            'transformer': lambda val, key, classee: [sm.OLS, [], {'hasconst': None}],
        },
    }
