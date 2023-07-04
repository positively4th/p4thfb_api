import ramda as R
import numpy as np
import numbers
from math import isnan

from contrib.pyas.src.pyas_v3 import As

from src.common.error import Error
from src.features.featurcontext import FeatureContext
from src.mixins.event.eventcontext import EventContext
from src.mixins.classidentified import ClassIdentified
from src.tools.numpy import Numpy as NP


class FeatureMatrix:

    prototypes = []

    @classmethod
    def onNew(cls, self):
        pass

    @classmethod
    def vectorizeEvents(cls, events, FeatureClasses, fallbackValues=[]):

        errors = []
        if len(FeatureClasses) == 0:
            return np.zeros((len(events), len(FeatureClasses))), []

        X = np.full(shape=(len(events), len(FeatureClasses)),
                    fill_value=None)
        dtypes = [set([]) for i in range(len(FeatureClasses))]
        for r, event in enumerate(events):
            for c, featureCreator in enumerate(FeatureClasses):
                feature = featureCreator(event)
                try:
                    try:
                        v = feature.value
                        if v is None or (isinstance(v, numbers.Number) and isnan(v)):
                            raise Exception('Feature cannot be computed.')
                    except Exception as e:
                        if len(fallbackValues) > 0:
                            v = fallbackValues[c % len(fallbackValues)]
                        else:
                            raise Error(e, instance=feature, method='value', ContextClasses=[
                                        As(FeatureContext)])
                    X[r][c] = v if v is not None else np.nan
                    dtypes[c].add(v.__class__)
                except Error as error:
                    eventContext = {
                        'instance': event
                    }
                    As(EventContext)(eventContext)
                    errors.append(error.extend({
                        **{
                            'row': r + 1,
                            'col': c + 1,
                        },
                        **eventContext
                    }))

        dtypes = R.map(lambda dt: NP.pythonTypes2NumpyType(dt))(dtypes)
        X = np.array([(*x,) for x in X], dtype={
            'names': [ClassIdentified.id(FeatureClass) for FeatureClass in FeatureClasses],
            'formats': dtypes
        })
        return X, errors

    @classmethod
    def _keepMatrixRows(cls, X, skipRowIndexes):
        sIndexes = set(skipRowIndexes)
        if len(X.shape) > 1 and X.shape[1] == 0:
            return np.zeros((X.shape[0] - len(sIndexes), 0))
        skipMap = dict(zip(sIndexes, sIndexes))
        rows = []
        for r in range(X.shape[0]):
            if r + 1 in skipMap:
                continue
            rows.append(X[r])

        # print(len(rows), X.shape[0], len(sIndexes))
        assert len(rows) == X.shape[0] - len(sIndexes)
        res = np.array(rows, dtype=X.dtype)
        return res

    @classmethod
    def faultyRowIndexSet(cls, errors):
        return set(
            R.pipe(
                R.map(lambda e: e.context['row']),
                R.uniq,
            )(errors)
        )
