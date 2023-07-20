from estimators.logistic_v1 import Logistic
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from features.outcome.goal_v1 import OutcomeGoal
from features.one_v1 import One
from features.oppgoal.width_v1 import Width
from features.oppgoal.distance_v1 import Distance
from features.oppgoal.probblockgoalie_v1 import ProbBlockGoalie
from features.oppgoal.probblockdefenders_v1 import ProbBlockDefenders
from features.isheader_v1 import IsHeader


class LogisticXG(Leaf):

    prototypes = [
        Logistic, *Logistic.prototypes
    ]

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
