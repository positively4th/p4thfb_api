from contrib.pyas.src.pyas_v3 import Leaf

from mixins.context.context import Context


class MatrixContext(Leaf):

    prototypes = [Context] + Context.prototypes

    columnSpecs = {
        'row': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'col': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }
