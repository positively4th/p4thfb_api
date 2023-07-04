from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T

from src.mixins.node import createNode


class EstimationNode(Leaf):

    prototypes = [createNode(nodesKey='estimationNodes', leafKey='estimate')]

    columnSpecs = {
        'id': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'name': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'estimate': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'estimationNodes': {
            'transformer': T.defWrapper([], lambda val, key, classee: val),
        },
        'results': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'meta': {
            'transformer': T.defWrapper({}, lambda val, key, classee: val),
        },
        'N': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }

    @property
    def isEmpty(self):
        return len(self['estimationNodes']) < 1 and 'esimate' not in self

    def trySquashSingleChild(self):
        if len(self['estimationNodes']) != 1:
            return {**self.row}

        child = self['estimationNodes'][0]
        if self.row['id'] != child['id']:
            return {**self.row}

        return {**self.row, **child}
