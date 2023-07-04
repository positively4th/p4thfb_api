from flask import jsonify

from contrib.pyas.src.pyas_v3 import As

from src.mappers.estimator.estimatormapper import EstimatorMapper
from src.tools.python import Python


def routes(estimatorDB):

    def estimators():
        estimators = Python.retry(lambda: As(EstimatorMapper)({}).load(estimatorDB(), jiffs=False),
                                  Python.createFixedSleeper(1.0, 10))
        for estimator in estimators:
            del estimator['cls']
        return jsonify(estimators)

    return {
        '': (estimators, (), {}),
    }
