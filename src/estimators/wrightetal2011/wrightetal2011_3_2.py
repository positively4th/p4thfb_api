from statsmodels.discrete import discrete_model as dm
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T
from src.estimators.estimator import Estimator
from src.estimators.logistic import Logistic
from estimators.predictors.statsmodelspredictor import StatsModelsPredictor
from src.features.one import One
from src.features.outcome.goal import OutcomeGoal
from src.features.wrightetal2011.pos import POS2
from src.features.wrightetal2011.pos import POS5
from src.features.wrightetal2011.tos import TOSBody
from src.features.wrightetal2011.pdsg import PDSG3_5
from src.features.wrightetal2011.pdsg import PDSG6_8
from src.features.wrightetal2011.gkp import GKP18Yard
from src.features.wrightetal2011.pof import POF5


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
