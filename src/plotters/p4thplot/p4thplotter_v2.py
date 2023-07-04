

from contrib.pyas.src.pyas_v3 import T
from contrib.p4thpyplot.src.tools import Tools as P4thPlotTools

from src.plotters.plotter_v2 import Plotter


class P4thPlotter:

    prototypes = [Plotter] + Plotter.prototypes

    columnSpecs = {
        'newColorGetter': {
            'transformer': T.generator(lambda *_, **__: P4thPlotTools.createColorGetter()),
        },
        'newMarkerGetter': {
            'transformer': T.generator(lambda *_, **__: P4thPlotTools.createMarkerGetter()),
        },
    }

    @classmethod
    def onNew(cls, self):
        pass

    def createFeatureRowPicker(self, featureId, *_, fallback=None, **__):

        if featureId is None:
            return None

        return lambda row, *_, **__: row[featureId] if featureId in row else fallback

    def createFeatureColorRowPicker(self, featureId, *_, **__):

        if featureId is None:
            return None

        colorGetter = self['newColorGetter']

        return lambda row, *_, **__: colorGetter(row[featureId])

    def createFeatureMarkerRowPicker(self, featureId=None, *_, **__):

        if featureId is None:
            return None

        markerGetter = self['newMarkerGetter']

        return lambda row, *_, **__: markerGetter(row[featureId])
