import numpy as np


from src.mixins.log import Log


class FeatureMatrix:

    prototypes = [Log] + Log.prototypes

    @classmethod
    def _keepMatrixRows(cls, X, skipRowIndexes):
        sIndexes = set(skipRowIndexes)
        if len(X.shape) > 1 and X.shape[1] == 0:
            return np.zeros((X.shape[0] - len(sIndexes), 0))
        skipMap = dict(zip(sIndexes, sIndexes))

        rows = [X[r] for r in range(X.shape[0]) if r + 1 not in skipMap]

        # print(len(rows), X.shape[0], len(sIndexes))
        assert len(rows) == X.shape[0] - len(sIndexes)
        res = np.array(rows, dtype=X.dtype)
        return res

    @classmethod
    def faultyRowIndexSet(cls, errors):
        return {e.context['row'] for e in errors}
