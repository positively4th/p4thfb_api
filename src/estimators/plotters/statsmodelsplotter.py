from contrib.pyas.src.pyas_v3 import Leaf
import io
import base64
from matplotlib import pyplot as plt

from statsmodels.api import graphics as smg

from src.tools.plot import Plot
from src.estimators.plotters.plotter import Plotter


class StatsModelsPlotter(Leaf):

    prototypes = [Plotter] + Plotter.prototypes

    columnSpecs = {
        'statsResultsClass': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }

    def deserializeResults(self, serialized):
        serializedResults = io.BytesIO(base64.decodebytes(serialized))
        res = self['statsResultsClass'].load(serializedResults)
        return res

    def _plot(self, estimationNode, plotName, args=[], argMap={}):

        assert 'results' in estimationNode
        results = estimationNode['results']
        results = self.deserializeResults(results)

        kwArgs = {}
        kwArgs.update(argMap)

        plot = getattr(smg, plotName)
        plt.rc("figure", figsize=(16, 8))
        fig = plot(results, *args, **kwArgs)
        fig.tight_layout(pad=1.0)
        return Plot.plotAsBase64(fig)
