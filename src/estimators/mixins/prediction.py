from contrib.pyas.src.pyas_v3 import Leaf

from src.estimators.mixins.predictionnode import PredictionNode


class Prediction(Leaf):

    prototypes = [PredictionNode] + PredictionNode.prototypes

    columnSpecs = {
        'jiff': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }
