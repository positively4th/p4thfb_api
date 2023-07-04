from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from src.estimators.logistic_v2 import Logistic
from src.features.one_v2 import One
from src.features.outcome.goal_v2 import OutcomeGoal
from src.features.wrightetal2011.pos_v2 import POS2
from src.features.wrightetal2011.pos_v2 import POS5
from src.features.wrightetal2011.tos_v2 import TOSBody
from src.features.wrightetal2011.pdsg_v2 import PDSG3_5
from src.features.wrightetal2011.pdsg_v2 import PDSG6_8
from src.features.wrightetal2011.gkp_v2 import GKP18Yard
from src.features.wrightetal2011.pof_v2 import POF5
from src.mixins.classidentified import ClassIdentified
from src.mixins.classnamed import ClassNamed


class WrightEtAl2011_3_2(Leaf):

    prototypes = [Logistic] + Logistic.prototypes + [ClassIdentified,
                                                     ClassNamed] + ClassIdentified.prototypes + ClassNamed.prototypes

    columnSpecs = {
        'YFeatureClasses': {
            'transformer': T.defWrapper(lambda *_: [
                As(OutcomeGoal),
            ], lambda val, key, classee: val if key in classee.row else None),
        },
        'XFeatureClasses': {
            'transformer': T.defWrapper(lambda *_: [
                As(One),
                As(POS2),
                As(POS5),
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
