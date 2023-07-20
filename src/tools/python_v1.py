
import inspect
from datetime import datetime
import dill
import numpy as np
from io import BytesIO
from math import isnan
from flask.json.provider import DefaultJSONProvider

from src.tools.python import Python as Python0
from src.tools.plot import Plot
from src.common.error import Error


class Python(Python0):


    class JSONProvider(DefaultJSONProvider):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        @classmethod
        def replace(cls, l, replacer):
            return [cls.replace(v, replacer) if isinstance(v, (list, tuple)) else replacer(v) for v in l]

        def default(self, obj):
            if isinstance(obj, Error):
                return obj.forJSON()
            if isinstance(obj, float) and isnan(obj):
                return None
            if isinstance(obj, Python.CSONWrapper):
                cson = obj.prepareForJSON()
                # print(cson)
                return cson
            if isinstance(obj, np.ndarray):
                return self.replace(obj.tolist(), lambda v: None if v != v else v)
            if isinstance(obj, datetime):
                return str(obj)
            obj = Plot.asJSON(obj)
            if isinstance(obj, dict):
                try:
                    return obj
                except ValueError as e:
                    # print(str(obj)[0:40])
                    # print(e)
                    return None
            if isinstance(obj, BytesIO):
                try:
                    return super().default(obj)
                except TypeError as e:
                    # print(str(obj)[0:40])
                    # print(e)
                    return None
            if inspect.isclass(obj):
                return dill.dumps(obj)

            try:
                return super().default(obj)
            except ValueError as e:
                # print(str(obj)[0:40])
                # print(e)
                return None
            except TypeError as e:
                # print(str(obj)[0:40])
                # print(e)
                return None


