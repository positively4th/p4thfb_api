import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.mappers.estimation.estimationmapper_v2 import EstimationMapper
from mappers.estimator.estimatormapper import EstimatorMapper as EstimatorMapper0


class EstimatorMapper(Leaf):

    prototypes = [EstimatorMapper0] + EstimatorMapper0.prototypes

    async def loadEstimations(self, estimatorDB, estimators, jiffs):
        estimatorIds = [
            e['estimatorId'] for e in estimators
        ]
        estimations = await As(EstimationMapper)({}).load(
            estimatorDB, estimatorIds, jiffs=jiffs)
        estimations = R.group_by(lambda est: est['estimatorId'])(estimations)
        for estimator in estimators:
            estimatorId = estimator['estimatorId']
            estimator['estimations'] = estimations[estimatorId] \
                if estimatorId in estimations else []

    async def load(self, estimatorDB, estimatorIds=None, jiffs=None):

        filterers = []
        if estimatorIds is not None:
            filterers.append(self.idFilterer(estimatorIds))
        estimators = self.getEstimators(filterers=filterers)

        # estimators = [As(estimator['cls'])({}) for estimator in estimators]
        if not jiffs is False:
            await self.loadEstimations(estimatorDB, estimators, jiffs)

        return estimators
