from statsmodels.discrete import discrete_model as dm

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.estimators.estimator import Estimator
from src.estimators.estimaters.statsmodelslogitestimater import StatsModelsLogitEstimater
from src.estimators.predictors.statsmodelslogitpredictor import StatsModelsLogitPredictor
from src.estimators.plotters.statsmodelslogitplotter import StatsModelsLogitPlotter


class Logistic:

    prototypes = [StatsModelsLogitEstimater] + StatsModelsLogitEstimater.prototypes \
        + [StatsModelsLogitPredictor] + StatsModelsLogitPredictor.prototypes \
        + [StatsModelsLogitPlotter] + StatsModelsLogitPlotter.prototypes \
        + [Estimator] + Estimator.prototypes
