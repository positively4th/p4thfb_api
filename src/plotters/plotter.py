import datetime
import pandas as pd
import ramda as R

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T

from contrib.p4thpymap.src.mappers import pdf

from src.mixins.versionguard import globalVersionGuard
from src.mixins.versionguard import VersionGuardMismatchError
from src.tools.python import Python
from src.features.feature import Feature
from src.mixins.classnamed import ClassNamed
from src.mixins.classidentified import ClassIdentified
from src.mixins.config.config import Config


class Plotter:

    prototypes = [ClassNamed] + [ClassIdentified] + \
        ClassNamed.prototypes + ClassIdentified.prototypes + \
        [globalVersionGuard()] + globalVersionGuard().prototypes

    columnSpecs = {
        'config': {
            'transformer': lambda val, key, classee: val if key in classee.row else classee.config,
        },
        'configMap': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else classee.configMap),
        },
        'FeatureClasses': {
            'transformer': lambda val, key, classee: val if key in classee.row else [],
        },
        'MetaFeatureClasses': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else []),
        },
        'plotNodes': {
            'transformer': T.defWrapper(lambda *args: [], lambda val, key, classee: val if key in classee.row else classee._allMetaFeatures()),
        },
        'errors': {
            'transformer': lambda val, key, classee: val if key in classee.row else [],
        },
    }

    allowUnapprovedVersion = False

    config = {}

    configMap = {}

    metaFeaurePaths = []

    @staticmethod
    def approveVersion(semanticVersion: tuple):
        return semanticVersion[0] == 3

    def _setMetaFeatureClasses(self, config, allFeaturesClasses):
        configee = As(Config)(config)

        features = []
        for path in self.metaFeaurePaths:
            featureId = configee.pick(path)
            if featureId is None:
                continue
            feature = R.find(
                lambda featureClass: ClassIdentified.id(
                    featureClass) == featureId
            )(allFeaturesClasses)
            if feature is not None:
                features.append(feature)

        self['MetaFeatureClasses'] = features

    @property
    def featureNames(self):
        return [As(Feature).featureName(F) for F in self['FeatureClasses'] + self['MetaFeatureClasses']]

    @property
    def featureIds(self):
        return [As(Feature).featureId(F) for F in self['FeatureClasses'] + self['MetaFeatureClasses']]

    @classmethod
    def getPlotters(cls, filterers=[]):

        def filterer(name, classInspect):

            if not issubclass(classInspect, (Leaf,)):
                return False

            try:
                ClassInspectee = As(classInspect)
            except VersionGuardMismatchError as e:
                print(classInspect.__name__, e)
                return False

            if not ClassInspectee.implements(Plotter):
                return False

            return True

        classSpecs = Python.getClasses('src/plotters/**/*.py', rootDir='.',
                                       filterers=[filterer] + filterers)
        res = []
        for classSpec in classSpecs:
            res.append({
                **classSpec,
                **{
                    'id': ClassIdentified.id(classSpec['cls']),
                    'name': ClassNamed.name(classSpec['cls']),
                },
            })
        return res

    @classmethod
    def onNew(cls, self):
        pass

    def updateConfig(self, config: dict,
                     allFeatureClasses: list = None,
                     selectedFeatureClasses: list = None,
                     events: list = None):
        if config is not None:
            self['config'] = config

        self._setMetaFeatureClasses(self['config'], allFeatureClasses)
        return self['config']

    def plotFromMatrix(self, X, errors, config=None):

        _config = self['config'] if config is None else config

        configMap = self['configMap']
        kwargs = self.mapConfigValues(configMap, As(Config)(_config))

        dfX = pd.DataFrame.from_records(X)

        dynTotWidth = min(pdf.colWidth2TotWidth(
            len(self.featureNames), 10), 160)

        plotNode = {
            'id': self.id(self),
            'name': self.name(self),
            'jiff': datetime.datetime.now(),
            'errors': [],
            'dataSummary': [],
        }
        dataSummary = []
        try:
            plotNode = self.plotter(plotNode, X, _config, **kwargs)
        except Exception as e:
            plotNode['errors'].append(str(e))

        try:
            dataSummary.append(pdf.format(pdf.aggregate(
                dfX, ['count', 'min', 'mean', 'median', 'max']).transpose(copy=True), colWidth=10))
        except Exception as e:
            errors.append({
                'message': 'Error in computing aggregates: {}'.format(str(e)),
                'exception': e,
            })

        try:
            if len(self.featureIds) > 0:
                dataSummary += [
                    '\n',
                    'Correlations',
                    pdf.format(pdf.correlation(dfX), totWidth=dynTotWidth),
                ]
        except Exception as e:
            errors.append({
                'message': 'Error in computing correlations: {}'.format(str(e)),
                'exception': e,
            })

        if len(dataSummary) > 0:
            plotNode['dataSummary'] = '\n'.join(
                dataSummary + plotNode['dataSummary'])

        plotNode['errors'] = errors + plotNode['errors']

        return plotNode

    def plotter(self, plotNode, X, config, *args, **kwargs):
        raise Exception('Not implemented')

    def mapConfigValues(self, configMap: dict, configee=None):

        _configee = As(Config)(self['config']) \
            if configee is None else configee

        kwargs = {}
        for cfgKey, spec in configMap.items():
            if isinstance(spec, tuple):
                spec = {'path': spec}

            path = spec['path']

            if 'pipeCreators' in spec:
                cfgVals = []
                cfgValMap = {}
                if isinstance(path, dict):
                    cfgValMap = {kwarg: _configee.pick(
                        path) for kwarg, path in path.items()}
                else:
                    cfgVals = [_configee.pick(path) for path in (
                        path if isinstance(path, list) else [path])]

                creators = spec['pipeCreators']
                creators = [creators] if callable(creators) else creators
                pipes = R.pipe(
                    R.map(lambda creator: creator(
                        *cfgVals, key=cfgKey, self=self, **cfgValMap)),
                    R.filter(lambda pipe: pipe is not None)
                )(creators)

                if len(pipes) == len(creators):
                    kwarg = R.pipe(*pipes)
                else:
                    kwarg = None
            else:
                kwarg = _configee.pick(path)

            if kwarg is None:
                continue

            kwargs[cfgKey] = kwarg

        return kwargs

    def createAddMetaFeatureClass(self, featureId, *_, **__):

        def helper(val, *args, **kwargs):
            return val

        if featureId is None:
            return helper

        Features = Feature.getFeatures(featureId=featureId)
        Features = Features[0]
        self['MetaFeatureClasses'] = R.uniq(
            self['MetaFeatureClasses'] + [Features['cls']])
        return helper
