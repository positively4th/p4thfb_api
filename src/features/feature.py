import numpy as np

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.mixins.versionguard import globalVersionGuard
from src.mixins.versionguard import VersionGuardMismatchError
from src.tools.linalg import LinAlg
from src.tools.python import Python
from src.mixins.event.event import Event
from src.mixins.classnamed import ClassNamed
from src.mixins.classidentified import ClassIdentified
from src.common.error import Error
from src.features.featurcontext import FeatureContext


class Feature:

    featuresCache = None

    prototypes = [ClassNamed] + [ClassIdentified] + \
        ClassNamed.prototypes + ClassIdentified.prototypes + \
        [globalVersionGuard()] + globalVersionGuard().prototypes

    approvedVersions = {
        'application': '==0.0.0',
    }
    allowUnapprovedVersion = False

    @staticmethod
    def onNewClass(cls):
        cls.verifyVersions()

    @staticmethod
    def onNew(cls, self):
        self._meta = []

    @classmethod
    def allFeatures(cls):
        if cls.featuresCache is None:
            cls.featuresCache = cls.getFeatures()
        return cls.featuresCache

    @classmethod
    def allFeaturesClasses(cls):
        if cls.featuresCache is None:
            cls.featuresCache = [
                f['cls'] for f in cls.allFeatures()
            ]
        return cls.featuresCache

    @classmethod
    def getFeatures(cls, featureId=None, featureNames=None, filterers=[]):

        def featureFilterer(name, classInspect):
            if not issubclass(classInspect, (Leaf,)):
                return False

            try:
                ClassInspectee = As(classInspect)
            except VersionGuardMismatchError as e:
                print(classInspect.__name__, e)
                return False

            if not ClassInspectee.implements(Feature):
                return False

            if ClassNamed.name(ClassInspectee) is None:
                return False
            if ClassNamed.name(classInspect) is None:
                return False
            if featureId and featureId != ClassIdentified.id(ClassInspectee):
                return False
            return True

        classSpecs = Python.getClasses(
            'src/features/**/*.py', rootDir='.', filterers=[featureFilterer]+filterers)
        res = []
        for classSpec in classSpecs:
            classSpec['cls'] = As(classSpec['cls']) if issubclass(
                classSpec['cls'], (Leaf,)) else classSpec['cls']
            res.append({
                **classSpec,
                **{
                    'featureId': ClassIdentified.id(classSpec['cls']),
                    'featureName': ClassNamed.name(classSpec['cls'])
                },
            })
        return res

    @ classmethod
    def asList(cls, listish):
        if isinstance(listish, np.ndarray):
            return listish.tolist()
        return list(listish)

    def addMetaArrow(self, p, d, Ts=[]):
        self._meta.append({
            'type': 'arrow',
            'p': self.asList(LinAlg.transform(p, *Ts)),
            'd': self.asList(LinAlg.transform(d, *Ts)),
        })

    def addMetaArea(self, ps, fillColor=None, borderColor=None, Ts=[]):
        self._meta.append({
            'type': 'area',
            'fillColor': fillColor,
            'borderColor': borderColor,
            'ps': [self.asList(LinAlg.transform(p, *Ts)) for p in ps],
        })

    def addMetaAnnotation(self, p, text, Ts=[]):
        self._meta.append({
            'type': 'annotation',
            'p': self.asList(LinAlg.transform(p, *Ts)),
            'text': text,
        })

    def addMetaKeyVal(self, key, val):
        self._meta.append({
            'type': 'keyval',
            'key': key,
            'val': val,
        })

    @property
    @Error.errorize(ContextClasses=FeatureContext, prefix='value')
    def value(self):
        return None

    @property
    def meta(self):
        return self._meta

    @property
    def event(self):
        return self.row

    @event.setter
    def event(self, e):
        self.row = e

    @property
    def eventee(self):
        return As(Event)(self.event)

    @staticmethod
    def featureId(cls):
        return ClassIdentified.id(cls)

    @staticmethod
    def featureName(cls):
        return ClassNamed.name(cls)


def FeatureAsStr(val: Feature | str, inverse=False):
    if inverse:
        F = Feature.getFeatures(val)
        return As(F[0]['cls']) if len(F) == 1 else None
    return val.featureId(val)
