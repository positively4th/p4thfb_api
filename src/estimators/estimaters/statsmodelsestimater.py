import io
import base64
import numpy as np
import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.features.feature import Feature
from src.tools.numpy import Numpy as NP
from src.estimators.estimator import Estimator


class StatsModelsEstimater(Leaf):

    prototypes = []

    columnSpecs = {
        'statsModel': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }

    @property
    def xNames(self):
        return [As(Feature).featureName(F) for F in self['XFeatureClasses']]

    @property
    def yNames(self):
        return [As(Feature).featureName(F) for F in self['YFeatureClasses']]

    @property
    def xIds(self):
        return [As(Feature).featureId(F) for F in self['XFeatureClasses']]

    @property
    def yIds(self):
        return [As(Feature).featureId(F) for F in self['YFeatureClasses']]

    def serializeResult(self, results):

        pickledBytes = io.BytesIO()
        results.save(pickledBytes)
        pickledBytes.seek(0)
        return base64.encodebytes(pickledBytes.read())

    def estimater(self, X, Y):

        sm = self['statsModel']
        XFeatureClasses = self['XFeatureClasses']
        YFeatureClasses = self['YFeatureClasses']
        estimationNodes = [
            {
                'id': As(Feature).featureId(YFeatureClasses[i]),
                'name': As(Feature).featureName(YFeatureClasses[i]),
                'N': X.shape[0],
                'errors': As(Estimator).collectErrors(self['errors'], [self.yIds[i]] + self.xIds)
            } for i, col in enumerate(NP.columnNames(Y))

        ]

        for i, estimationNode in enumerate(estimationNodes):
            yId = As(Feature).featureId(YFeatureClasses[i])
            estimationNode['model'] = sm[0](
                Y[yId], NP.asArray(X), *sm[1], **sm[2])
            estimationNode['yName'] = self.yNames[i]
            estimationNode['xNames'] = self.xNames
            estimationNode['model'].exog_names[:] = self.xNames
            # setattr(estimationNode['estimator'], 'endog_names', yNames[i])
            estimationNode['results'] = estimationNode['model'].fit()
            estimationNode['estimationNodes'] = [
                {
                    'id': As(Feature).featureId(XFeatureClasses[i]),
                    'name': As(Feature).featureName(XFeatureClasses[i]),
                    'estimate': c,
                } for i, c in enumerate(estimationNode['results'].params)
            ]
            estimationNode['meta'] = self.createMetas(
                estimationNode, Y[yId], X)

        for i, estimationNode in enumerate(estimationNodes):
            estimationNode['results'] = self.serializeResult(
                estimationNode['results'])
            del estimationNode['model']

        return estimationNodes

    def createMetas(self, estimationNode, y, X):
        model = estimationNode['model']
        results = estimationNode['results']
        yName = estimationNode['yName']
        xNames = estimationNode['xNames']
        meta = []

        meta.append({
            'metaType': 'score',
            'title': 'Score',
            'score': model.score(results.params),
        })

        meta.append({
            'metaType': 'plainText',
            'title': 'Summary',
            'plainText': str(results.summary(yName, xNames)),
        })

        if hasattr(results, 'pred_table'):
            categories = sorted(np.unique(y.tolist()))
            if categories is None:
                categories = ['', estimationNode['name']]
                meta.append({
                    'metaType': 'matrix',
                    'title': 'Confusion Matrix',
                    'topRow': ['Predicted'] + categories,
                    'leftColumn': ['True'] + categories,
                    'matrix': results.pred_table(),

                })

        meta.append({
            'metaType': 'plot',
            'title': 'Partial Correlations Plot',
            'plotName': 'plot_partregress_grid',
            'args': [],
            'argMap': {},
        })

        if hasattr(results, 'get_influence'):
            meta.append({
                'metaType': 'plot',
                'title': 'Influence Plot',
                'plotName': 'influence_plot',
                'args': [],
                'argMap': {
                    'criterion': 'cooks',
                },
            })

        return meta
