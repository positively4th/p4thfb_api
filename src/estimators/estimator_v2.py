import datetime
from typing import List, Set, Tuple
import pandas as pd
import ramda as R

from contrib.p4thpymisc.src.misc import HashCache
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from src.mixins.versionguard import globalVersionGuard
from src.estimators.mixins.predictionnode import PredictionNode
from src.estimators.mixins.estimationnode import EstimationNode
from src.estimators.mixins.plotnode import PlotNode
from src.features.feature_v2 import Feature
from src.features.featurematrix_v2 import FeatureMatrix
from src.mixins.classnamed import ClassNamed
from src.mixins.classidentified import ClassIdentified
from src.common.error import Error


class Estimator:

    prototypes = [ClassNamed] + [ClassIdentified] + \
        ClassNamed.prototypes + ClassIdentified.prototypes + \
        [globalVersionGuard()] + globalVersionGuard().prototypes

    columnSpecs = {
        'XFeatureClasses': {
            'transformer': lambda val, key, classee: val if key in classee.row else [],
        },
        'YFeatureClasses': {
            'transformer': lambda val, key, classee: val if key in classee.row else [],
        },
        'estimations': {
            'transformer': T.defWrapper(lambda *args: [], lambda val, key, classee: val),
        },
        'predictions': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'errors': {
            'transformer': lambda val, key, classee: val if key in classee.row else [],
        },
    }

    approvedVersions = {
        'application': '==1.0.0',
    }

    @staticmethod
    def createEventCache():

        def serialize(events, _):
            xored = R.reduce(
                lambda res, event: res ^ int(event['__id'])
            )(0, events)
            return str(xored)

        return HashCache(serializer=serialize, hasher=lambda x: x)

    @classmethod
    def onNew(cls, self):
        self.keyCache = cls.createEventCache()
        self.XCache = HashCache()
        self.YCache = HashCache()

    async def getX(self, events):
        key = self.keyCache.key(events)
        X = self.XCache.get(key)
        if X is not None:
            return X
        res = await FeatureMatrix.vectorizeEvents(events, self['XFeatureClasses'])
        self.XCache.set(key, res)
        return res

    async def getY(self, events):
        key = self.keyCache.key(events)
        Y = self.YCache.get(key)
        if Y is not None:
            return Y
        res = await FeatureMatrix.vectorizeEvents(events, self['YFeatureClasses'])
        self.YCache.set(key, res)
        return res

    @classmethod
    def estimatorId(cls):
        return ClassIdentified.id(cls)

    @classmethod
    def estimatorName(cls):
        return ClassNamed.name(cls)

    @classmethod
    def estimatorNameOrId(cls):
        if hasattr(cls, 'estimatorName'):
            return cls.estimatorName()
        return cls.estimatorId()

    @classmethod
    def collectErrors(cls, errors: List[Error] | Tuple[Error] | Set[Error], featureIds):

        def filterer(e: Error):
            ctx = e.context
            if 'featureId' not in ctx:
                return False
            return e.context['featureId'] in featureIds

        res = R.pipe(
            R.filter(filterer),
            R.map(lambda e: e.forJSON()),
        )(errors)
        return res

    def predicter(self, estimationNode, X):
        raise Exception('Not implemented')

    def plotter(self, estimationNode, plotName, args=[], argMap={}, estimationNodeId=None):
        raise Exception('Not implemented')

    async def predict(self, events, estimation):
        X, errors = await FeatureMatrix.vectorizeEvents(
            events, self['XFeatureClasses'], fallbackValues=[])

        # print('X', X)
        # assert errors == []
        return As(EstimationNode)(estimation).map(
            T=lambda e: (self.predicter(e, X), 'predictionNodes'),
            nodeFilterer=lambda pNode: As(EstimationNode).Skip if As(
                PredictionNode)(pNode).isEmpty else pNode
        )

    def plot(self, estimation, plotName, args=[], argMap=[], estimationNodeId=None):

        # print('X', X)
        # assert errors == []
        return As(EstimationNode)(estimation).map(
            T=lambda estimationNode: (
                self.plotter(estimationNode, plotName, args=args,
                             argMap=argMap, estimationNodeId=estimationNodeId)
            ),
            nodeFilterer=lambda pNode: As(EstimationNode).Skip if As(
                PlotNode)(pNode).isEmpty else pNode
        )

    def describe(self, classList, matrix):
        if len(classList) == 0:
            return 'No columns'
        df = pd.DataFrame(matrix, columns=[
            Feature.featureName(C) for C in classList])

        print(df.describe())

    def describeX(self, events):
        X, errorsX = self.getX(events)
        self.describe(self['XFeatureClasses'], X)

    def describeY(self, events):
        Y, errorsY = self.getY(events)
        self.describe(self['YFeatureClasses'], Y)

    async def estimate(self, events):

        X, errorsX = await self.getX(events)
        Y, errorsY = await self.getY(events)

        self['errors'] = self['errors'] + errorsX + errorsY

        estimation = {
            'id': self.estimatorId(),
            'name': self.estimatorNameOrId(),
            'jiff': datetime.datetime.now(),
            'estimationNodes': self.estimater(
                FeatureMatrix._keepMatrixRows(
                    X, As(FeatureMatrix).faultyRowIndexSet(self['errors'])),
                FeatureMatrix._keepMatrixRows(
                    Y, As(FeatureMatrix).faultyRowIndexSet(self['errors'])),
            )
        }
        self['estimations'].append(estimation)
        return estimation

    def estimater(self, id, name, X, Y):
        raise Exception('Not implemented')

    def getEstimation(self, jiff):

        def matcher(estimationNode):
            return 'jiff' in estimationNode and estimationNode['jiff'] == jiff

        return R.find(matcher)(self['estimations'])
