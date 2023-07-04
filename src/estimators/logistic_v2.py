from src.estimators.estimator_v2 import Estimator
from src.estimators.estimaters.statsmodelslogitestimater import StatsModelsLogitEstimater
from src.estimators.predictors.statsmodelslogitpredictor import StatsModelsLogitPredictor
from src.estimators.plotters.statsmodelslogitplotter import StatsModelsLogitPlotter


class Logistic:

    prototypes = [StatsModelsLogitEstimater] + StatsModelsLogitEstimater.prototypes \
        + [StatsModelsLogitPredictor] + StatsModelsLogitPredictor.prototypes \
        + [StatsModelsLogitPlotter] + StatsModelsLogitPlotter.prototypes \
        + [Estimator] + Estimator.prototypes
