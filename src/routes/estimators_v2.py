from quart import jsonify

from contrib.pyas.src.pyas_v3 import As

from src.mappers.estimator.estimatormapper_v2 import EstimatorMapper
from src.tools.python_v2 import Python


def routes(estimatorDB):

    async def estimators():
        def helper():
            return As(EstimatorMapper)({}).load(estimatorDB(), jiffs=False)

        estimators = await Python.retry_async(helper,
                                              Python.createFixedSleeper(1.0, 10))
        for estimator in estimators:
            del estimator['cls']
        return jsonify(estimators)

    return {
        '/': (estimators, (), {}),
    }
