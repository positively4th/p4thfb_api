
from collections.abc import Callable
import inspect
import glob
import importlib
from datetime import datetime
import time
import dill
import numpy as np
import ramda as R
from json import JSONEncoder, dumps
from io import BytesIO
from math import isnan
from flask.json.provider import DefaultJSONProvider

from contrib.p4thcson.src.cson import cson
from src.tools.plot import Plot
from src.common.error import Error


class _JSONProvider(DefaultJSONProvider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def replace(cls, l, replacer):
        return [cls.replace(v, replacer) if isinstance(v, (list, tuple)) else replacer(v) for v in l]

    @staticmethod
    def default(obj):
        from src.features.feature_v2 import Feature
        from src.features.feature_v2 import FeatureAsStr

        if isinstance(obj, Feature):
            return FeatureAsStr(obj)
        if isinstance(obj, Error):
            return obj.forJSON()
        if isinstance(obj, float) and isnan(obj):
            return None
        if isinstance(obj, CSONWrapper):
            cson = obj.prepareForJSON()
            # print(cson)
            return cson
        if isinstance(obj, np.ndarray):
            return _JSONProvider.replace(obj.tolist(), lambda v: None if v != v else v)
        if isinstance(obj, datetime):
            return str(obj)
        obj = Plot.asJSON(obj)
        if isinstance(obj, dict):
            try:
                return obj
                return JSONEncoder.default(self, obj)
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
            return obj.__dict__
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


class CSONWrapper:

    def __init__(self, thing):
        self.thing = thing

    def prepareForJSON(self):
        return cson.asUncircular(self.thing)


class Python():

    @staticmethod
    def createFixedSleeper(delay: float, retries: int):

        def helper(e: Exception):

            nonlocal retries

            if retries < 0:
                raise e

            retries = retries - 1
            time.sleep(delay)

        return helper

    @classmethod
    def retry(cls, f, sleeper):
        try:
            return f()
        except Exception as e:
            sleeper(e)

        return cls.retry(f, sleeper)

    @classmethod
    def getClasses(cls, globPattern, rootDir=None, filterers=[]):
        pyFiles = glob.glob(globPattern, root_dir=rootDir, recursive=True)
        classes = []
        for pyFile in pyFiles:
            modPath = pyFile.replace('/', '.')[:-3]
            try:
                mod = importlib.import_module(modPath)

                nameClassPairs = inspect.getmembers(mod, inspect.isclass)
                for name, cls in nameClassPairs:
                    if R.find(lambda filterer: not filterer(name, cls))(filterers):
                        continue
                    classes.append({
                        'path': modPath,
                        'className': name,
                        'cls': cls,
                    })
            except ModuleNotFoundError as e:
                print(e)
        return classes

    @classmethod
    def dumps(cls, thing):
        dumps(thing, cls=cls.JSONEncoder())

    @staticmethod
    def JSONProvider():

        from flask.json.provider import DefaultJSONProvider

        class _(DefaultJSONProvider):

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
                if isinstance(obj, CSONWrapper):
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
                        return JSONEncoder.default(self, obj)
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

    @staticmethod
    def JSONEncoder():

        class _(JSONEncoder):

            @classmethod
            def replace(cls, l, replacer):
                return [cls.replace(v, replacer) if isinstance(v, (list, tuple)) else replacer(v) for v in l]

            def default(self, obj):
                if isinstance(obj, Error):
                    return obj.forJSON()
                if isinstance(obj, float) and isnan(obj):
                    return None
                if isinstance(obj, CSONWrapper):
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
                        return JSONEncoder.default(self, obj)
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

        return _

    @classmethod
    def createCache(size, noVal=None):

        cache = {}

        def helper(key, val=noVal):
            if val is noVal:
                return cache[key] if key in cache else noVal
            else:
                cache[key] = val
            return val

        return helper
