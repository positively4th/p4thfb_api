from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T

from src.mixins.node import createNode


class PredictionNode(Leaf):

    prototypes = [createNode(nodesKey='predictionNodes', leafKey='prediction')]

    columnSpecs = {
        'id': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'name': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'jiff': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'prediction': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'predictionNodes': {
            'transformer': T.defWrapper(lambda *args: [], lambda val, key, classee: val),
        },
    }

    @property
    def isEmpty(self):
        return len(self['predictionNodes']) < 1 and 'prediction' not in self.row
