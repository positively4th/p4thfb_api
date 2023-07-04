import numpy as np
import ramda as R

from numpy.lib.recfunctions import structured_to_unstructured


class Numpy:

    @classmethod
    def asArray(cls, X: np.array):
        dtypes = R.pipe(
            R.map(lambda dt: dt[1]),
            R.uniq,
        )(X.dtype.descr)

        dtype = X.dtype[0]
        if len(dtypes) == 2 and '<i8' in dtypes and '<f8' in dtypes:
            dtype = '<f8'

        return structured_to_unstructured(X, dtype=dtype, copy=True)

    @classmethod
    def columnNames(cls, arr: np.array):
        return arr.dtype.names if (hasattr(arr, 'dtype') and hasattr(arr.dtype, 'names')) else None

    @classmethod
    def pythonTypes2NumpyType(cls, ts: set):

        if str in ts or np.str_ in ts:
            return 'O'
        elif int in ts or np.int_ in ts:
            return '<f8'

        return ts.pop() if len(ts) == 1 else None
