import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.mixins.versionguard import VersionGuardMismatchError
from src.mixins.classidentified import ClassIdentified
from src.mixins.classnamed import ClassNamed
from src.tools.python_v2 import Python
from src.mappers.estimation.estimationmapper_v2 import EstimationMapper
from src.estimators.estimator_v2 import Estimator


class EstimatorMapper(Leaf):

    @staticmethod
    def idFilterer(ids):

        def helper(name, classInspect):
            ClassInspectee = As(classInspect)
            if not ClassIdentified.id(ClassInspectee) in ids:
                return False
            return True

        return helper

    @classmethod
    def getEstimators(cls, filterers=[]):

        def filterer(name, classInspect):

            if not issubclass(classInspect, (Leaf,)):
                return False

            try:
                ClassInspectee = As(classInspect)
            except VersionGuardMismatchError as e:
                print(classInspect.__name__, e)
                return False

            # methodNames = [name for name, _ in inspect.getmembers(
            #     ClassInspectee, inspect.ismethod)]

            if not issubclass(ClassInspectee, (Estimator,)):
                return False

            if ClassIdentified.id(ClassInspectee) is None:
                return False

            return True

        classSpecs = Python.getClasses('src/estimators/**/*.py', rootDir='.',
                                       filterers=[filterer] + filterers)
        res = []
        for classSpec in classSpecs:
            res.append({
                **classSpec,
                **{
                    'estimatorId': ClassIdentified.id(As(classSpec['cls'])),
                    'estimatorName': ClassNamed.name(As(classSpec['cls']))
                },
            })
        return res

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
