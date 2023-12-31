import os.path

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from src.tools.python_v2 import Python
from src.store.store import Store


class _AutoStores(Leaf):

    prototypes = []

    columnSpecs = {}

    db = None

    @classmethod
    def setDBs(cls, db):
        cls.db = db

    @classmethod
    def getStores(cls):

        def storeFilterer(name, classInspect):
            if not issubclass(classInspect, (Leaf,)):
                return False

            ClassInspectee = As(classInspect)

            if not ClassInspectee.implements(Store):
                return False

            return True

        rootPath = os.path.dirname(__file__)

        classSpecs = Python.getClasses(
            '**/*.py'.format(rootPath), rootDir=rootPath, filterers=[storeFilterer])
        res = []
        for classSpec in classSpecs:
            classSpec['cls'] = As(classSpec['cls']) if issubclass(
                classSpec['cls'], (Leaf,)) else classSpec['cls']
            res.append({
                **classSpec,
            })
        return res

    @classmethod
    def onNew(cls, self):

        def createColumnSpec(StoreClass):
            storee = As(StoreClass)(
                {**{'db': cls.db}, **self.row})
            return {
                'transformer': T.virtual(lambda key, val, classee: storee)
            }

        allStores = cls.getStores()
        for s in allStores:
            name = s['className']
            name = name[0].lower() + name[1:]
            self.__class__.columnSpecs[name] = createColumnSpec(s['cls'])


def setAutoStoresDBs(db):
    _AutoStores.setDBs(db)


def getAutoStores(_autoStores=[]):
    if len(_autoStores) < 1:
        _autoStores.append(As(_AutoStores)({}))

    return _autoStores[0]
