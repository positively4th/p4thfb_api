import datetime
import importlib
from flask import jsonify
from flask import request
from json import dumps

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thcson.src.cson import cson

from src.tools.python_v1 import Python
from src.common.filter import Filter
from src.mappers.event.eventmapper import EventMapper
from src.estimators.estimator_v1 import Estimator
from mappers.estimator.estimatormapper_v1 import EstimatorMapper
from src.mappers.estimation.estimationmapper_v1 import EstimationMapper


def routes(statDB, estimatorDB, estimatorCacheLock=None):

    noVal = None
    estimatorCache = Python.createCache(noVal=noVal)

    def loadEstimator(estimatorId):

        nonlocal estimatorCache

        with estimatorCacheLock:
            estimator = estimatorCache(estimatorId)
            if estimator is noVal:
                estimator = Python.retry(lambda: As(EstimatorMapper)({}).load(estimatorDB(), estimatorIds=[estimatorId]),
                                         Python.createFixedSleeper(1.0, 5))
                assert len(estimator) == 1
                estimator = estimator[0]
                estimatorCache(estimatorId, estimator)
        return estimator

    def estimator(estimatorId):

        estimator = loadEstimator(estimatorId)

        return jsonify(estimator)

    def predict(estimatorId, jiff):
        estimator = loadEstimator(estimatorId)
        estimation = As(Estimator)(estimator).getEstimation(
            datetime.datetime.fromisoformat(jiff))
        if estimation is None or estimation['state'] != 'ready':
            return jsonify(None)
        estimator.update({
            'XFeatureClasses': estimation['XFeatureClasses'],
            'YFeatureClasses': estimation['YFeatureClasses'],

        })

        payload = cson.fromJSON(dumps(request.json))
        events = payload['events']

        estimatoree = As(estimator['cls'])(estimator)
        res = estimatoree.predict(events, estimation)

        return jsonify({
            'result': res
        })

    def plot(estimatorId, jiff, estimationNodeId, plotName):
        estimator = loadEstimator(estimatorId)
        estimation = As(Estimator)(estimator).getEstimation(
            datetime.datetime.fromisoformat(jiff))
        if estimation is None or estimation['state'] != 'ready':
            return jsonify(None)

        estimator.update({
            'XFeatureClasses': estimation['XFeatureClasses'],
            'YFeatureClasses': estimation['YFeatureClasses'],

        })

        payload = cson.fromJSON(dumps(request.json))
        args = payload['args'] if 'args' in payload else []
        argMap = payload['argMap'] if 'argMap' in payload else {}
        estimatoree = As(estimator['cls'])(estimator)
        res = estimatoree.plot(estimation, plotName, args=args,
                               argMap=argMap, estimationNodeId=estimationNodeId)

        return jsonify({
            'result': res
        })

    def estimate(estimatorId):
        payload = request.json
        featureFilter = payload['featureFilter']

        # XFeatureClasses = [
        #    spec['cls'] for spec in Feature.getFeatures(
        #        featureNames=featureFilter['xFeatures'])
        # ]
        # YFeatureClasses = [
        #    spec['cls'] for spec in Feature.getFeatures(
        #        featureNames=featureFilter['yFeatures'])
        # ]
        estimator = As(EstimatorMapper)({}).load(
            estimatorDB(), estimatorIds=[estimatorId])
        assert len(estimator) == 1
        estimator = estimator[0]
        # estimator.update({
        #    'XFeatureClasses': XFeatureClasses,
        #    'YFeatureClasses': YFeatureClasses,
        # })

        # Estimator = getattr(importlib.import_module(
        #     estimator['path'], estimator['module']), estimator['className'])
        Estimator = estimator['cls']
        estimatoree = As(Estimator)(estimator)

        estimation = {
            'jiff': datetime.datetime.now(),
            'estimatorId': estimatorId,
            'XFeatureClasses': estimatoree['XFeatureClasses'],
            'YFeatureClasses': estimatoree['YFeatureClasses'],
            'eventIds': [],
            'state': 'running',
            'error': '',
        }
        As(EstimationMapper)({}).save(estimatorDB(), [estimation])

        try:
            filteree = As(Filter)(payload['eventFilter'])
            pq = Filter.eventFilter, {}
            pq = filteree.apply(statDB.createPipes(), pq)
            events = As(EventMapper)({}).load(statDB, pq)
            estimation.update({
                'eventIds': [e['__id'] for e in events],
            })

            estimation = {
                **estimation,
                **estimatoree.estimate(events),
                **{'jiff': estimation['jiff']},
            }

            estimation.update({
                'state': 'ready',
                'error': '',
            })
            As(EstimationMapper)({}).save(estimatorDB(), [estimation])
        except Exception as e:
            estimation.update({
                'state': 'failed',
                'error': str(e),
            })
            As(EstimationMapper)({}).save(estimatorDB(), [estimation])
            raise e
        return jsonify(estimate)

    return {
        '/<estimatorId>': (estimator, (), {}),
        '/estimate/<estimatorId>': (estimate, (), {'methods': ['POST']}),
        '/predict/<estimatorId>/<jiff>': (predict, (), {'methods': ['POST']}),
        '/plot/<estimatorId>/<jiff>/<estimationNodeId>/<plotName>': (plot, (), {'methods': ['POST']}),
    }
