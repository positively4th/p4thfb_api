import numpy as np
import ramda as R

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.mixins.versionguard import globalVersionGuard
from src.mixins.versionguard import VersionGuardMismatchError
from src.tools.linalg import LinAlg
from src.mixins.classnamed import ClassNamed
from src.mixins.classidentified import ClassIdentified
from src.tools.python_v2 import Python


class Feature:

    classSpecCache = None
    featuresCache = None
    featureAsStrCache = {}

    prototypes = [ClassNamed] + [ClassIdentified] + \
        ClassNamed.prototypes + ClassIdentified.prototypes + \
        [globalVersionGuard()] + globalVersionGuard().prototypes

    allowUnapprovedVersion = False

    @classmethod
    def onNew(cls, self):
        self._meta = []

    @staticmethod
    def onNewClass(cls):
        cls.verifyVersions()

    @classmethod
    def allFeatures(cls):
        if cls.featuresCache is None:
            cls.featuresCache = cls.getFeatures()
        return cls.featuresCache

    @classmethod
    def allFeaturesClasses(cls):
        return [f['cls'] for f in cls.allFeatures()]

    @staticmethod
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
        return True

    @classmethod
    def getCachedClassSpecs(cls):

        if cls.classSpecCache is None:

            cls.classSpecCache = []

            classSpecs = Python.getClasses(
                'src/features/**/*.py', rootDir='.', filterers=[cls.featureFilterer])
            for classSpec in classSpecs:

                cls.classSpecCache.append({
                    **classSpec,
                })

        return cls.classSpecCache

    @classmethod
    def getFeatures(cls, featureId=None, featureNames=None, filterers=[]):

        def featureFilterer(name, ClassInspectee):

            if featureId and featureId != ClassIdentified.id(ClassInspectee):
                return False

            if featureNames and ClassNamed.name(ClassInspectee) not in featureNames:
                return False
            return True

        classSpecs = cls.getCachedClassSpecs()

        res = []
        for classSpec in classSpecs:
            classee = As(classSpec['cls']) if issubclass(
                classSpec['cls'], (Leaf,)) else classSpec['cls']
            if R.find(
                lambda filterer: not filterer(classSpec['className'], classee)
            )([featureFilterer]+filterers):
                continue
            res.append({
                **classSpec,
                **{
                    'cls': classee,
                    'featureId': ClassIdentified.id(classee),
                    'featureName': ClassNamed.name(classee)
                },
            })
        return res

    @classmethod
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
        raise 'Not implemented'

    @staticmethod
    def featureId(cls):
        return ClassIdentified.id(cls)

    @staticmethod
    def featureName(cls):
        return ClassNamed.name(cls)

    @classmethod
    def createFeatureAsStr(cls, cache: dict = None):

        _cache = cls.featureAsStrCache if cache is None else cache

        def featureAsStr(val: Feature | str, inverse=False):
            if inverse:
                if val not in _cache:
                    F = cls.getFeatures(val)
                    _cache[val] = As(F[0]['cls']) if len(F) == 1 else None
                return _cache[val]

            return val.featureId(val)

        return featureAsStr
