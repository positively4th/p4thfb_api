from typing import List, Set, Tuple
import pandas as pd
import ramda as R

from contrib.p4thpymisc.src.misc import HashCache
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from src.mixins.versionguard import globalVersionGuard
from src.estimators.mixins.estimationnode import EstimationNode
from src.estimators.mixins.plotnode import PlotNode
from src.features.feature import Feature
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

    def getX(self, events):
        raise Exception('Not implemented.')

    def getY(self, events):
        raise Exception('Not implemented.')

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

    def predict(self, events, estimation):
        raise Exception('Not implemented')

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
            As(Feature).featureName(C) for C in classList])

        print(df.describe())

    def describeX(self, events):
        raise Exception('Not implemented')

    def describeY(self, events):
        raise Exception('Not implemented')

    def estimate(self, events):
        raise Exception('Not implemented')

    def estimater(self, id, name, X, Y):
        raise Exception('Not implemented')

    def getEstimation(self, jiff):

        def matcher(estimationNode):
            return 'jiff' in estimationNode and estimationNode['jiff'] == jiff

        return R.find(matcher)(self['estimations'])
