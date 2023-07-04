from statsmodels.discrete import discrete_model as dm

from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.estimaters.statsmodelsestimater import StatsModelsEstimater


class StatsModelsLogitEstimater(Leaf):

    prototypes = [StatsModelsEstimater] + StatsModelsEstimater.prototypes

    columnSpecs = {
        'statsModel': {
            'transformer': lambda val, key, classee: [dm.Logit, [], {'missing': 'raise', 'check_rank': True}],
        },
    }
