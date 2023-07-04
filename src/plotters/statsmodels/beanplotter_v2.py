import numpy as np
from statsmodels.graphics.boxplots import beanplot

from contrib.pyas.src.pyas_v3 import Leaf

from src.tools.numpy import Numpy as NP
from src.plotters.statsmodels.statsmodelsplotter_v2 import StatsmodelsPlotter


class BeanPlotter(Leaf):

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
            'jitter': {
                'value': True,
                'error': None,
                'spec': {
                    'specType': 'CategorySpec',
                    'label': 'Jitter',
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
        'jitter': ('jitter',),
    }

    @staticmethod
    def approveVersion(semanticVersion: tuple):
        return semanticVersion[0] == 3

    @classmethod
    def onNew(cls, self):
        pass

    def plotter(self, plotNode, X: np.recarray, config, *args, **kwargs):

        cols = len(self['FeatureClasses'])

        data = [NP.asArray(X)[:, col].tolist() for col in range(cols)]
        labels = self.featureNames

        fig = beanplot(*args, data=data, labels=labels, **kwargs)

        plotNode['plot'] = fig

        return plotNode
