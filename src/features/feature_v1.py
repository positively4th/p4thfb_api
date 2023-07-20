
from contrib.pyas.src.pyas_v3 import As

from src.mixins.event.event_v1 import Event
from src.common.error import Error
from src.features.feature import Feature as Feature0
from src.features.featurcontext import FeatureContext


class Feature:

    prototypes = [Feature0] + Feature0.prototypes

    approvedVersions = {
        'application': '==0.0.0',
    }

    # @staticmethod
    # def featureFilterer(name, classInspect):
    #     if not issubclass(classInspect, (Leaf,)):
    #         return False

    #     try:
    #         ClassInspectee = As(classInspect)
    #     except VersionGuardMismatchError as e:
    #         print(classInspect.__name__, e)
    #         return False

    #     if not ClassInspectee.implements(Feature):
    #         return False

    #     if ClassNamed.name(ClassInspectee) is None:
    #         return False
    #     if ClassNamed.name(classInspect) is None:
    #         return False
    #     return True

    @property
    @Error.errorize(ContextClasses=FeatureContext, prefix='value')
    def value(self):
        return None

    @property
    def eventee(self):
        return As(Event)(self.event)
