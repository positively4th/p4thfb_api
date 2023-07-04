import ramda as R
import datetime
from quart import jsonify
from quart import request
from json import dumps

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thcson.src.cson import cson

from src.tools.python_v2 import Python
from src.common.filter import Filter
from src.estimators.estimator_v2 import Estimator
from src.mappers.estimator.estimatormapper_v2 import EstimatorMapper
from src.mappers.estimation.estimationmapper_v2 import EstimationMapper
from src.store.event.eventstore import EventStore
from src.store.autostores import getAutoStores


def routes(statDB, estimatorDB):

    noVal = None
    estimatorCache = Python.createCache(noVal=noVal)

    stores = getAutoStores()

    async def loadEstimator(estimatorId):

        async def loadWrapper(): return await As(EstimatorMapper)({}).load(
            estimatorDB(), estimatorIds=[estimatorId])

        nonlocal estimatorCache

        estimator = estimatorCache(estimatorId)
        if estimator is noVal:
            estimator = await Python.retry_async(loadWrapper, Python.createFixedSleeper(1.0, 5))
            assert len(estimator) == 1
            estimator = estimator[0]
            estimatorCache(estimatorId, estimator)
        return estimator

    async def estimator(estimatorId):

        estimator = await loadEstimator(estimatorId)

        return jsonify(estimator)

    async def predict(estimatorId, jiff):
        estimator = await loadEstimator(estimatorId)
        estimation = As(estimator['cls'])(estimator).getEstimation(
            datetime.datetime.fromisoformat(jiff))
        if estimation is None or estimation['state'] != 'ready':
            return jsonify(None)
        estimator.update({
            'XFeatureClasses': estimation['XFeatureClasses'],
            'YFeatureClasses': estimation['YFeatureClasses'],

        })

        payload = cson.fromJSON(dumps(await request.json))
        events = payload['events']

        estimatoree = As(estimator['cls'])(estimator)
        res = await estimatoree.predict(events, estimation)

        return jsonify({
            'result': res
        })

    async def plot(estimatorId, jiff, estimationNodeId, plotName):
        estimator = await loadEstimator(estimatorId)
        estimation = As(Estimator)(estimator).getEstimation(
            datetime.datetime.fromisoformat(jiff))
        if estimation is None or estimation['state'] != 'ready':
            return jsonify(None)

        estimator.update({
            'XFeatureClasses': estimation['XFeatureClasses'],
            'YFeatureClasses': estimation['YFeatureClasses'],

        })

        payload = cson.fromJSON(dumps(await request.json))
        args = payload['args'] if 'args' in payload else []
        argMap = payload['argMap'] if 'argMap' in payload else {}
        estimatoree = As(estimator['cls'])(estimator)
        res = estimatoree.plot(estimation, plotName, args=args,
                               argMap=argMap, estimationNodeId=estimationNodeId)

        return jsonify({
            'result': res
        })

    async def estimate(estimatorId):
        payload = await request.json
        # featureFilter = payload['featureFilter']
        # XFeatureClasses = [
        #    spec['cls'] for spec in Feature.getFeatures(
        #        featureNames=featureFilter['xFeatures'])
        # ]
        # YFeatureClasses = [
        #    spec['cls'] for spec in Feature.getFeatures(
        #        featureNames=featureFilter['yFeatures'])
        # ]
        estimator = await As(EstimatorMapper)({}).load(
            estimatorDB(), estimatorIds=[estimatorId])
        assert len(estimator) == 1
        estimator = estimator[0]
        # estimator.update({
        #    'XFeatureClasses': XFeatureClasses,
        #    'YFeatureClasses': YFeatureClasses,
        # })

        # Estimator = getattr(importlib.import_module(
        #     estimator['path']), estimator['className'])
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
        await As(EstimationMapper)({}).save(estimatorDB(), [estimation])

        try:
            eventStoree = As(EventStore)({**stores['eventStore']})

            filteree = As(Filter)(payload['eventFilter'])
            qp = Filter.eventFilter, {}
            qp = filteree.apply(statDB.createPipes(), qp)
            rows = await statDB.query(qp)
            ids = [r['__id'] for r in rows]
            events = R.unnest((await eventStoree.get(ids)).values())

            estimation.update({
                'eventIds': [e['__id'] for e in events],
            })

            estimation = {
                **estimation,
                **(await estimatoree.estimate(events)),
                **{'jiff': estimation['jiff']},
            }

            estimation.update({
                'state': 'ready',
                'error': '',
            })
            await As(EstimationMapper)({}).save(estimatorDB(), [estimation])
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
