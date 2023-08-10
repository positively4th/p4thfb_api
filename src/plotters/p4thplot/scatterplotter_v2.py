import numpy as np

import pandas as pd
import ramda as R

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T
from contrib.p4thpyplot.src.scatterplot import ScatterPlot

from src.mixins.classnamed import ClassNamed
from src.mixins.classidentified import ClassIdentified
from src.plotters.p4thplot.p4thplotter_v2 import P4thPlotter
from src.mixins.config.config import Config
from src.plotters.plotter_v2 import Plotter


class ScatterPlotter(Leaf):

    prototypes = [P4thPlotter] + P4thPlotter.prototypes

    columnSpecs = {
    }

    config = {
        'spec': {
            'specType': 'ConfigMapSpec',
            'allowedTypes': [dict()],
        },
        'error': None,
        'value': {
            'markerSize': {
                'value': None,
                'error': None,
                'spec': {
                    'specType': 'ValueSpec',
                    'allowedTypes': [1, 0.1, None],
                    'label': 'Marker Size',
                },
            },
            'text': {
                'value': None,
                'error': None,
                'spec': {
                    'specType': 'CategorySpec',
                    'allowedTypes': ['', None],
                    'label': 'Point text',
                    'valueMetas': None
                },
            },
            'color': {
                'value': None,
                'error': None,
                'spec': {
                    'specType': 'CategorySpec',
                    'allowedTypes': ['', None],
                    'label': 'Color',
                    'valueMetas': None
                },
            },
            'marker': {
                'value': None,
                'error': None,
                'spec': {
                    'specType': 'CategorySpec',
                    'allowedTypes': ['', None],
                    'label': 'Marker',
                    'valueMetas': None
                },
            },
            'olsWidth': {
                'value': None,
                'error': None,
                'spec': {
                    'specType': 'ValueSpec',
                    'allowedTypes': [int(1), float(1.1), None],
                    'label': 'Least Squares Width',
                },
            },
            'olsGroups': {
                'value': None,
                'error': None,
                'spec': {
                    'specType': 'CategorySpec',
                    'allowedTypes': ['', None],
                    'label': 'Least Squares Groups',
                    'valueMetas': None
                },
            },

        },
    }

    metaFeaurePaths = [('text',), ('color',), [('marker',)], ('olsGroups',)]

    configMap = {
        'markerSize': ('markerSize',),
        'text': {
            'path': ('text',),
            'pipeCreators': (
                lambda featureId, key, self: self.createFeatureRowPicker(
                    featureId),
                lambda value, key, self: None if value is None else str,
            )
        },
        'color': {
            'path': ('color',),
            'pipeCreators': (
                lambda value, key, self: self.createFeatureColorRowPicker(
                    value, key),
            )
        },
        'marker': {
            'path': [('marker',)],
            'pipeCreators': (
                lambda value, key, self: self.createFeatureMarkerRowPicker(
                    value, key),
            )
        },
        'ols': {
            'path': {
                'featureId': ('olsGroups',),
                'lineWidth': ('olsWidth',)
            },
            'pipeCreators': (
                lambda *args, key, self, **kwargs: self.createFeatureOLS(
                    *args, **kwargs),
            )
        }
    }

    @classmethod
    def onNew(cls, self):
        pass

    def updateConfig(self, config: dict,
                     allFeatureClasses: list = None,
                     selectedFeatureClasses: list = None,
                     events: list = None):

        def featureClass(config):
            if allFeatureClasses is None:
                return config
            configee = As(Config)(config)
            specee = configee.specee

            if not specee.row['valueMetas']:
                specee['valueMetas'] = [
                    {
                        'value':  ClassIdentified.id(FeatureClass),
                        'label': ClassNamed.name(FeatureClass)
                    }
                    for FeatureClass in allFeatureClasses
                ]

            return config

        self['config'] = super().updateConfig(config,
                                              allFeatureClasses=allFeatureClasses,
                                              selectedFeatureClasses=selectedFeatureClasses,
                                              events=events)
        configee = As(Config)(self['config'])

        configee['value']['text'] = featureClass(configee['value']['text'])
        configee['value']['color'] = featureClass(configee['value']['color'])
        configee['value']['marker'] = featureClass(configee['value']['marker'])
        configee['value']['olsGroups'] = featureClass(
            configee['value']['olsGroups'])

        return self['config']

    def plotter(self, plotNode, X: np.recarray, config, *args, **kwargs):

        configee = As(Config)(config)

        def plotX(plotNode, FeatureClassY, FeatureClassX):

            nonlocal df

            xName = ClassNamed.name(FeatureClassX)
            yName = ClassNamed.name(FeatureClassY)
            xId = ClassIdentified.id(FeatureClassX)
            yId = ClassIdentified.id(FeatureClassY)

            axis, fig = ScatterPlot.plot(df, *args, xLabel=xName, yLabel=yName,
                                         x=lambda row, *_, **__: row[xId],
                                         y=lambda row, *_, **__: row[yId], **kwargs)

            plotNode['plot'] = fig
            plotNode['name'] = ' x '.join([
                ClassNamed.name(FeatureClassX),
                ClassNamed.name(FeatureClassY),
            ])
            plotNode['id'] = ' '.join([
                plotNode['id'],
                ClassIdentified.id(FeatureClassX),
                ClassIdentified.id(FeatureClassY),
            ])
            return plotNode

        def plotY(plotNode, FeatureClassY, FeatureClasses):

            plotNodes = [plotX(dict(plotNode), FeatureClassY, FeatureClass)
                         for i, FeatureClass in enumerate(FeatureClasses)]

            plotNode['plotNodes'] = plotNodes
            plotNode['name'] = ' '.join([
                ClassNamed.name(FeatureClassY)
            ])
            return plotNode

        FeatureClasses = self['FeatureClasses']
        df = pd.DataFrame.from_records(X, columns=self.featureIds)
        plotNodes = [
            plotY(dict(plotNode), FeatureClass, FeatureClasses[i+1:])
            for i, FeatureClass in enumerate(FeatureClasses)
            if i < len(FeatureClasses) - 1
        ]
        plotNode['plotNodes'] = plotNodes
        return plotNode

    def createFeatureOLS(self, featureId=None, lineWidth=1, color='gold', alpha=1.0):

        def ols(rows, iis, xs, ys, *_, **__):
            template = {
                'alpha': alpha,
                'linewidth': lineWidth,
                'color': color,
            }

            featureIds = [None] if featureId is None else R.pipe(
                R.map(lambda row: row[featureId]),
                R.uniq
            )(rows)

            res = [
                {
                    **template,
                    **{
                        'xys': [(xs[i], ys[i]) for i in iis if fid is None or rows[i][featureId] == fid],
                    }
                }
                for fid in featureIds
            ]
            return res

        return ols
