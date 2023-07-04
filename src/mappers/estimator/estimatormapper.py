import inspect
import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.mixins.versionguard import VersionGuardMismatchError
from src.tools.python import Python
from src.mappers.estimation.estimationmapper import EstimationMapper


class EstimatorMapper(Leaf):

    @staticmethod
    def idFilterer(ids):

        def helper(name, classInspectee):
            if not classInspectee.estimatorId() in ids:
                return False
            return True

        return helper

    @classmethod
    def getEstimators(cls, filterers=[]):

        def filterer(name, classInspectee):
            methodNames = [name for name, _ in inspect.getmembers(
                classInspectee, inspect.ismethod)]

            if not issubclass(classInspectee, (Leaf,)):
                return False

            try:
                As(classInspectee)
            except VersionGuardMismatchError as e:
                print(classInspectee.__name__, e)
                return False

            if not 'estimatorName' in methodNames:
                return False
            return True

        classSpecs = Python.getClasses('src/estimators/**/*.py', rootDir='.',
                                       filterers=[filterer] + filterers)
        res = []
        for classSpec in classSpecs:
            res.append({
                **classSpec,
                **{
                    'estimatorId': classSpec['cls'].estimatorId(),
                    'estimatorName': classSpec['cls'].estimatorName()
                },
            })
        return res

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
