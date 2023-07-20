import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.mappers.estimation.estimationmapper_v1 import EstimationMapper
from src.mappers.estimator.estimatormapper import EstimatorMapper as EstimatorMapper0


class EstimatorMapper(Leaf):

    prototypes = [EstimatorMapper0] + EstimatorMapper0.prototypes

    def loadEstimations(self, estimatorDB, estimators, jiffs):
        estimatorIds = [
            e['estimatorId'] for e in estimators
        ]
        estimations = As(EstimationMapper)({}).load(
            estimatorDB, estimatorIds, jiffs=jiffs)
        estimations = R.group_by(lambda est: est['estimatorId'])(estimations)
        for estimator in estimators:
            estimatorId = estimator['estimatorId']
            estimator['estimations'] = estimations[estimatorId] \
                if estimatorId in estimations else []

    def load(self, estimatorDB, estimatorIds=None, jiffs=None):

        filterers = []
        if estimatorIds is not None:
            filterers.append(self.idFilterer(estimatorIds))
        estimators = self.getEstimators(filterers=filterers)

        if not jiffs is False:
            self.loadEstimations(estimatorDB, estimators, jiffs)

        return estimators
