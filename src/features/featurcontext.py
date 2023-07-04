from contrib.pyas.src.pyas_v3 import Leaf

from src.mixins.context.context import Context
from src.mixins.classidentified import ClassIdentified
from src.mixins.classnamed import ClassNamed


class FeatureContext(Leaf):

    prototypes = [Context] + Context.prototypes

    columnSpecs = {
        'featureName': {
            'transformer': lambda val, key, classee, self, cls: ClassNamed.name(self),
        },
        'featureId': {
            'transformer': lambda val, key, classee, self, cls: ClassIdentified.id(self),
        },
    }

    @classmethod
    def onNew(cls, self):
        feature = self['instance']
        delta = Context.extendIfMissing(self.row, {
            'featureId': feature.id(feature),
            'featureName': feature.name(feature),
        })
        for k, v in delta.items():
            self[k] = v
