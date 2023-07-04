from contrib.pyas.src.pyas_v3 import T


class Context():

    prototypes = []

    columnSpecs = {
        'errorType': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else 'Unspecified Error'),
        },
        'instance': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },
        'method': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },
        'arguments': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },
        'argumentsMap': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },
    }

    @staticmethod
    def extendIfMissing(target: dict, delta: dict):
        delta = {k: v for (k, v) in delta.items()
                 if k not in target or target[k] is None}
        return {
            **target,
            **delta
        }

    def forJSON(self):
        return {
            k: v.forJSON() if hasattr(v, 'forJSON') else v for k, v in self.row.items() if k != 'instance'
        }
