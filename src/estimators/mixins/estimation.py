from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.mixins.estimationnode import EstimationNode


class Estimation(Leaf):

    prototypes = [EstimationNode] + EstimationNode.prototypes

    columnSpecs = {
        'jiff': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }
