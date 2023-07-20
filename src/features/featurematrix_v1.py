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
from src.features.featurematrix import FeatureMatrix as FeatureMatrix0


class FeatureMatrix:

    prototypes = [FeatureMatrix0] + FeatureMatrix0.prototypes

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
