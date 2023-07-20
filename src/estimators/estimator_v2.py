import datetime

from contrib.pyas.src.pyas_v3 import As

from src.estimators.mixins.predictionnode import PredictionNode
from src.estimators.mixins.estimationnode import EstimationNode
from src.features.featurematrix_v2 import FeatureMatrix
from src.estimators.estimator import Estimator as Estimator0
from src.mixins.classidentified import ClassIdentified
from src.mixins.classnamed import ClassNamed


class Estimator:

    prototypes = [
        Estimator0, *Estimator0.prototypes,
        ClassIdentified, ClassNamed, *ClassIdentified.prototypes, *ClassNamed.prototypes,
    ]

    approvedVersions = {
        'application': '==1.0.0',
    }

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

    async def predict(self, events, estimation):
        X, errors = await FeatureMatrix.vectorizeEvents(
            events, self['XFeatureClasses'], fallbackValues=[])

        return As(EstimationNode)(estimation).map(
            T=lambda e: (self.predicter(e, X), 'predictionNodes'),
            nodeFilterer=lambda pNode: As(EstimationNode).Skip if As(
                PredictionNode)(pNode).isEmpty else pNode
        )

    async def describeX(self, events):
        X, errorsX = await self.getX(events)
        self.describe(self['XFeatureClasses'], X)

    async def describeY(self, events):
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
                As(FeatureMatrix)._keepMatrixRows(
                    X, As(FeatureMatrix).faultyRowIndexSet(self['errors'])),
                As(FeatureMatrix)._keepMatrixRows(
                    Y, As(FeatureMatrix).faultyRowIndexSet(self['errors'])),
            )
        }
        self['estimations'].append(estimation)
        return estimation
