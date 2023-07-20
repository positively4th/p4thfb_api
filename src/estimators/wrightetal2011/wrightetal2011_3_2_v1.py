from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from src.estimators.logistic_v1 import Logistic
from features.one_v1 import One
from features.outcome.goal_v1 import OutcomeGoal
from features.wrightetal2011.pos_v1 import POS2
from features.wrightetal2011.pos_v1 import POS5
from features.wrightetal2011.tos_v1 import TOSBody
from features.wrightetal2011.pdsg_v1 import PDSG3_5
from features.wrightetal2011.pdsg_v1 import PDSG6_8
from features.wrightetal2011.gkp_v1 import GKP18Yard
from features.wrightetal2011.pof_v1 import POF5


class WrightEtAl2011_3_2(Leaf):

    prototypes = [Logistic] + Logistic.prototypes

    columnSpecs = {
        'YFeatureClasses': {
            'transformer': T.defWrapper(lambda *_: [
                As(OutcomeGoal),
            ], lambda val, key, classee: val if key in classee.row else None),
        },
        'XFeatureClasses': {
            'transformer': T.defWrapper(lambda *_: [
                As(One),
                As(POS5),
                As(POS2),
                As(TOSBody),
                As(PDSG3_5),
                As(PDSG6_8),
                As(GKP18Yard),
                As(POF5),
            ], lambda val, key, classee: val if key in classee.row else None),
        },

    }

    @classmethod
    def onNew(cls, self):
        pass

    @classmethod
    def estimatorId(cls):
        return WrightEtAl2011_3_2.__name__

    @classmethod
    def estimatorName(cls):
        return WrightEtAl2011_3_2.__name__
