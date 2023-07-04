from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T

from src.mixins.node import createNode


class PlotNode(Leaf):

    prototypes = [createNode(nodesKey='plotNodes', leafKey='plot')]

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
        'dataSummary': {
            'transformer': lambda val, key, classee: val if key in classee.row else '',
        },
        'plot': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'plotNodes': {
            'transformer': T.defWrapper(lambda *args: [], lambda val, key, classee: val),
        },
    }

    @property
    def isEmpty(self):
        return len(self['plotNodes']) < 1 and 'plot' not in self.row
