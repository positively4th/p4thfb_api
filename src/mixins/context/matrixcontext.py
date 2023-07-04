from contrib.pyas.src.pyas_v3 import Leaf

from src.mixins.context.context import Context


class MatrixContext():

    prototypes = [Context] + Context.prototypes

    columnSpecs = {
        'row': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'column': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }
