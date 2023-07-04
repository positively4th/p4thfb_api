from statsmodels.graphics.boxplots import violinplot

from contrib.pyas.src.pyas_v3 import Leaf

from src.plotters.statsmodels.statsmodelsplotter import StatsmodelsPlotter
from src.tools.numpy import Numpy as NP


class ViolinPlotter(Leaf):

    prototypes = [StatsmodelsPlotter] + StatsmodelsPlotter.prototypes

    columnSpecs = {}

    config = {
        'spec': {
            'specType': 'ConfigMapSpec',
            'allowedTypes': [dict()],
        },
        'error': None,
        'value': {
            'side': {
                'value': 'both',
                'error': None,
                'spec': {
                    'specType': 'CategorySpec',
                    'allowedTypes': [str(),],
                    'label': 'Side',
                    'valueMetas': [
                        {'value': 'left', 'label': 'Left side'},
                        {'value': 'right', 'label': 'Right side'},
                        {'value': 'both', 'label': 'Both sides'},
                    ]
                },
            },
            'show_boxplot': {
                'value': True,
                'error': None,
                'spec': {
                    'specType': 'CategorySpec',
                    'label': 'Show Boxplot',
                    'allowedTypes': [bool(),],
                    'valueMetas': [
                        {'value': True, 'label': 'Yes'},
                        {'value': False, 'label': 'No'},
                    ]
                },
            },
        },
    }

    configMap = {
        'side': ('side',),
        'show_boxplot': ('show_boxplot',),
    }

    @classmethod
    def onNew(cls, self):
        pass

    def plotter(self, plotNode, X, config, *args, **kwargs):

        cols = len(self['FeatureClasses'])

        data = NP.asArray(X)
        data = [data[:, col].tolist() for col in range(cols)]
        labels = self.featureNames

        fig = violinplot(*args, data=data, labels=labels, **kwargs)

        plotNode['plot'] = fig

        return plotNode
