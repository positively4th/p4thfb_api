from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T

from src.estimators.logistic_v2 import Logistic
from src.features.outcome.goal_v2 import OutcomeGoal
from src.features.one_v2 import One
from src.features.oppgoal.width_v2 import Width
from src.features.oppgoal.distance_v2 import Distance
from src.features.oppgoal.probblockgoalie_v2 import ProbBlockGoalie
from src.features.oppgoal.probblockdefenders_v2 import ProbBlockDefenders
from src.features.isheader_v2 import IsHeader
from src.mixins.classidentified import ClassIdentified
from src.mixins.classnamed import ClassNamed


class LogisticXG(Leaf):

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
                As(IsHeader),
                As(Distance),
                As(Width),
                As(ProbBlockGoalie),
                As(ProbBlockDefenders),
            ], lambda val, key, classee: val if key in classee.row else None),
        },
    }
