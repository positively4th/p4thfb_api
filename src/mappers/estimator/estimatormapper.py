import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.mixins.versionguard import VersionGuardMismatchError
from src.mixins.classidentified import ClassIdentified
from src.mixins.classnamed import ClassNamed
from src.tools.python import Python
from src.estimators.estimator import Estimator


class EstimatorMapper:

    prototypes = []

    classSpecCache = None

    @staticmethod
    def idFilterer(ids):

        def helper(name, ClassInspectee):
            if not ClassIdentified.id(ClassInspectee) in ids:
                return False
            return True

        return helper

    @staticmethod
    def filterer(name, classInspect):

        if not issubclass(classInspect, (Leaf,)):
            return False

        try:
            ClassInspectee = As(classInspect)
        except VersionGuardMismatchError as e:
            # print(classInspect.__name__, e)
            return False

        if not issubclass(ClassInspectee, (Estimator,)):
            return False

        return True

    @classmethod
    def getCachedClassSpecs(cls):

        if cls.classSpecCache is None:

            cls.classSpecCache = []

            classSpecs = Python.getClasses('src/estimators/**/*.py', rootDir='.',
                                           filterers=[cls.filterer])
            for classSpec in classSpecs:
                cls.classSpecCache.append({
                    **classSpec,
                    **{
                        'estimatorId': ClassIdentified.id(As(classSpec['cls'])),
                        'estimatorName': ClassNamed.name(As(classSpec['cls']))
                    },
                })

        return cls.classSpecCache

    @classmethod
    def getEstimators(cls, filterers=[]):

        classSpecs = cls.getCachedClassSpecs()

        res = []
        for classSpec in classSpecs:
            classee = As(classSpec['cls']) if issubclass(
                classSpec['cls'], (Leaf,)) else classSpec['cls']

            if R.find(
                lambda filterer: not filterer(classSpec['className'], classee)
            )(filterers):
                continue

            res.append({
                **classSpec,
                **{
                    'cls': classee,
                    'estimatorId': ClassIdentified.id(As(classSpec['cls'])),
                    'estimatorName': ClassNamed.name(As(classSpec['cls']))
                },
            })
        return res

    def loadEstimations(self, estimatorDB, estimators, jiffs):
        raise Exception('Not implemented')

    def load(self, estimatorDB, estimatorIds=None, jiffs=None):
        raise Exception('Not implemented')
