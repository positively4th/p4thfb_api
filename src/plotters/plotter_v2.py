from contrib.pyas.src.pyas_v3 import As

from src.features.featurematrix_v2 import FeatureMatrix
from plotters.plotter import Plotter as Plotter0


class Plotter:

    prototypes = [Plotter0] + Plotter0.prototypes

    approvedVersions = {
        'application': '==1.0.0',
    }

    async def plot(self, events, config=None):

        X, errors = await FeatureMatrix.vectorizeEvents(
            events, self['FeatureClasses'] + self['MetaFeatureClasses'])
        X = As(FeatureMatrix)._keepMatrixRows(
            X, As(FeatureMatrix).faultyRowIndexSet(errors))

        return self.plotFromMatrix(X, errors, config)
