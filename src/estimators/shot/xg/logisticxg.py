import numpy as np

from src.estimators.logistic import Logistic
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from src.features.outcome.goal import OutcomeGoal
from src.features.one import One
from src.features.oppgoal.width import Width
from src.features.oppgoal.distance import Distance
from src.features.oppgoal.probblockgoalie import ProbBlockGoalie
from src.features.oppgoal.probblockdefenders import ProbBlockDefenders
from src.features.isheader import IsHeader


class LogisticXG(Leaf):

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
                As(Distance),
                As(Width),
                As(ProbBlockGoalie),
                As(ProbBlockDefenders),
                As(IsHeader),
            ], lambda val, key, classee: val if key in classee.row else None),
        },
    }

    @classmethod
    def estimatorName(cls):
        return cls.__name__

    @classmethod
    def estimatorId(cls):
        return cls.__name__
