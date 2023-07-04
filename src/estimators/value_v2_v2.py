import datetime
import ramda as R
import asyncio

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.estimator_v2 import Estimator
from src.estimators.multilogistic_v2 import MultiLogistic as MultiLogisticEstimator
from src.estimators.ols_v2 import OLS as OLSEstimator
from src.estimators.mixins.estimationnode import EstimationNode
from mixins.event.event_v2 import Event
from src.features.feature_v2 import Feature
from src.features.one_v2 import One
from src.features.oppgoal.distance_v2 import Distance as OppGoalDistance
from src.features.oppgoal.probblockdefenders_v2 import ProbBlockDefenders as OppGoalProbBlockDefenders
from src.features.oppgoal.probblockgoalie_v2 import ProbBlockGoalie as OppGoalProbBlockGoalie
from src.features.oppgoal.width_v2 import Width as OppGoalWidth


def createEventGetter(id, map=None):
    if isinstance(id, dict) or id is None:
        return lambda: id

    return lambda: map[id]


def verifiedBool(val):
    if val == True:
        return int(1)
    if val == False:
        return int(0)
    raise ValueError('Not a bool!')


def verifiedFloat(val):
    return float(val)


def verifiedString(val):
    if isinstance(val, str):
        return val
    raise ValueError('Not a string!')


# noinspection PyAttributeOutsideInit
class OutcomeTypeFeature(Leaf):
    prototypes = [Feature] + Feature.prototypes

    @staticmethod
    def featureName(cls):
        return 'OutcomeType'

    @property
    async def value(self):
        return verifiedString(self['outcomeType'])
        try:
            verifiedString(self['outcomeType'])
        except Exception as e:
            pass
        f = asyncio.Future()
        f.set_result(
            verifiedString(self['outcomeType'])
        )
        return f


class xGOwn(Leaf):
    prototypes = [Feature] + Feature.prototypes

    @property
    async def value(self):
        return verifiedFloat(self['xGIfOwn'] / (1 - self['xGIfOwn']))


class xGOpp(Leaf):
    prototypes = [Feature] + Feature.prototypes

    @property
    async def value(self):
        return verifiedFloat(self['xGIfOpp'] / (1 - self['xGIfOpp']))


class ValueEvent(Leaf):
    prototypes = [Event] + Event.prototypes

    columnSpecs = {
        'outcomeEvent': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'outcomeType': {
            'transformer': lambda val, key, classee: val if key in classee.row else None
        },
        'xG': {
            'transformer': lambda val, key, classee: val if key in classee.row else None
        },
        'isShotOwn': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'isShotOpp': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'xGOwn': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'xGOpp': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },

    }


def createValueEstimator(id, name=None):
    class ValueEstimator(Leaf):

        @classmethod
        def estimatorId(cls):
            return id

        @classmethod
        def estimatorName(cls):
            return id if name is None else name

    return ValueEstimator


class Value(Leaf):
    prototypes = [Estimator] + Estimator.prototypes

    columnSpecs = {
        'estimate': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'estimators': {
            'transformer': lambda val, key, classee: val if key in classee.row else classee.estimators0(),
        },
        'sampleCount': {
            'transformer': lambda val, key, classee: val if key in classee.row else 100,
        },
    }

    def estimators0(self): return [
        As(createValueEstimator('Outcome Type'), MultiLogisticEstimator)({
            'XFeatureClasses': [
                As(One),
                As(OppGoalDistance),
                As(OppGoalWidth),
                As(OppGoalProbBlockDefenders),
                As(OppGoalProbBlockGoalie),
            ],
            'YFeatureClasses': [As(OutcomeTypeFeature)],
        }),
        As(createValueEstimator('xGOwn|Own Shot'), OLSEstimator)({
            'XFeatureClasses': [
                As(One),
                As(OppGoalDistance),
                As(OppGoalWidth),
                As(OppGoalProbBlockDefenders),
                As(OppGoalProbBlockGoalie),
            ],
            'YFeatureClasses': [As(xGOwn)],
        }),
        As(createValueEstimator('xGOpp|Opp Shot'), OLSEstimator)({
            'XFeatureClasses': [
                As(One),
                As(OppGoalDistance),
                As(OppGoalWidth),
                As(OppGoalProbBlockDefenders),
                As(OppGoalProbBlockGoalie),
            ],
            'YFeatureClasses': [As(xGOpp)],
        }),

    ]

    outcomeEventTypes = {
        As(Event).typeIdMap['Shot'],
        As(Event).typeIdMap['Half End'],
        As(Event).typeIdMap['Injury Stoppage']
    }

    valueEventTypes = {
        As(Event).typeIdMap['Shot'],
        As(Event).typeIdMap['Pass'],
        As(Event).typeIdMap['Carry']
    }

    def predict(self, events, estimation):

        prediction0 = {
            'id': self.estimatorId(),
            'name': self.estimatorName(),
            'jiff': estimation['jiff'],
            'predictionNodes': []
        }

        idEstimatorMap = R.index_by(
            lambda est: est.estimatorId())(self['estimators'])
        for estimationNode in estimation['estimationNodes']:
            id = As(EstimationNode)(estimationNode)['id']
            assert id in idEstimatorMap
            estimator = idEstimatorMap[id]
            prediction0['predictionNodes'].append(
                estimator.predict(events, estimationNode))

        return prediction0

    def plot(self, estimation, plotName, args=[], argMap=[], estimationNodeId=None):
        plotNode0 = {
            'id': self.estimatorId(),
            'name': self.estimatorName(),
            'jiff': estimation['jiff'],
            'estimationNodes': []
        }

        idEstimatorMap = R.index_by(
            lambda est: est.estimatorId())(self['estimators'])
        for estimationNode in estimation['estimationNodes']:
            id = As(EstimationNode)(estimationNode)['id']
            assert id in idEstimatorMap
            estimator = idEstimatorMap[id]
            plotNode0['estimationNodes'].append(estimator.plot(estimationNode, plotName,
                                                               args=args, argMap=argMap,
                                                               estimationNodeId=estimationNodeId))

        return plotNode0

    async def estimate(self, events):

        def _initOutcomeEvent():

            ses = R.sort_with([
                R.ascend(R.prop('matchId')),
                R.descend(R.prop('index')),
            ])(events)
            for i, event in enumerate(ses):
                if As(Event)(event)['typeId'] in self.outcomeEventTypes:
                    event['outcomeEvent'] = createEventGetter(event)
                    continue
                event['outcomeEvent'] = createEventGetter(
                    ses[i - 1]['outcomeEvent']()
                    if (i - 1 >= 0 and event['matchId'] == ses[i - 1]['matchId']) else None
                )

        async def _initOutcomes():

            async def getOutcome(event):
                res = {
                    'xG': None,
                    'outcomeType': None,
                    'sxG': None,
                    'xGIfOwn': None,
                    'xGIfOpp': None,
                }

                if not As(ValueEvent)(event)['typeId'] in self.valueEventTypes:
                    return res

                outcomeEvent = event['outcomeEvent']()
                if not outcomeEvent:
                    return res

                outcomeIsShot = As(Event)(outcomeEvent)[
                    'typeId'] == As(Event).typeIdMap['Shot']

                ownShot = outcomeIsShot and \
                    As(Event)(outcomeEvent)['eventTeamId'] == As(
                        Event)(event)['eventTeamId']
                oppShot = outcomeIsShot and \
                    As(Event)(outcomeEvent)['eventTeamId'] != As(
                        Event)(event)['eventTeamId']
                if not outcomeIsShot:
                    res['outcomeType'] = 'noShot'
                elif ownShot:
                    res['outcomeType'] = 'ownShot'
                elif oppShot:
                    res['outcomeType'] = 'oppShot'
                assert res['outcomeType'] is not None

                if not outcomeIsShot:
                    return res

                xG = verifiedFloat(await As(Event)(outcomeEvent).xG)
                res['xG'] = xG

                if (ownShot is not None) or (oppShot is not None):
                    sXG = sxG = (xG if ownShot else 0) - (xG if oppShot else 0)
                    res['sxG'] = sxG

                if ownShot:
                    xGIfOwn = xG
                    res['xGIfOwn'] = xGIfOwn

                if oppShot:
                    xGIfOpp = xG
                    res['xGIfOpp'] = xGIfOpp

                return res

            for event in events:
                event.update(await getOutcome(event))

        async def _estimate():

            estimationNodes = []
            for estimator in self['estimators']:
                print('Estimating {}:'.format(estimator.estimatorNameOrId()))
                estimationNode = await estimator.estimate(events)
                # estimationNode = As(EstimationNode)(estimationNode).trySquashSingleChild()
                estimationNodes.append(estimationNode)

            return estimationNodes

        _initOutcomeEvent()
        await _initOutcomes()

        esitmationNodes = await _estimate()
        estimation = {
            'id': self.estimatorId(),
            'name': self.estimatorNameOrId(),
            'jiff': datetime.datetime.now(),
            'estimationNodes': esitmationNodes,
        }
        self['estimations'].append(estimation)
        # print(self['estimates'])
        return estimation

    def summary(self):
        for estimator in self['estimators']:
            print(estimator['estimate'][0]['summary'])
