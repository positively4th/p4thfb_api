from contrib.pyas.src.pyas_v3 import Leaf

from src.mixins.classnamed import ClassNamed
from src.mixins.classidentified import ClassIdentified
from src.estimators.estimator import Estimator
from src.estimators.estimaters.statsmodelsolsestimater import StatsModelsOLSEstimater
from src.estimators.predictors.statsmodelsregressionpredictor import StatsModelsRegressionPredictor
from src.estimators.plotters.statsmodelsregressionplotter import StatsModelsRegressionPlotter


class OLS(Leaf):

    prototypes = [StatsModelsRegressionPlotter] + StatsModelsRegressionPlotter.prototypes \
        + [StatsModelsRegressionPredictor] + StatsModelsRegressionPredictor.prototypes \
        + [StatsModelsOLSEstimater] + StatsModelsOLSEstimater.prototypes \
        + [Estimator] + Estimator.prototypes \
        + [ClassIdentified, ClassNamed] \
        + ClassIdentified.prototypes + ClassNamed.prototypes

    columnSpecs = {}