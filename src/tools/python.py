import inspect
import glob
import importlib
import importlib.util
from datetime import datetime
import time
import os
import sys
import dill
import numpy as np
import ramda as R
from io import BytesIO
from math import isnan
from quart.json import dumps
from os.path import join
from contrib.p4thcson.src.cson import cson

from src.tools.plot import Plot
from src.common.error import Error




class Python():

    class CSONWrapper:

        def __init__(self, thing):
            self.thing = thing

        def prepareForJSON(self):
            return cson.asUncircular(self.thing)



    @staticmethod
    def isOwnModuleClass(module, cls) -> bool:
        return module.__name__ == cls.__module__

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
    async def retry_async(cls, f, sleeper):
        try:
            return await f()
        except Exception as e:
            sleeper(e)

        return await cls.retry(f, sleeper)

    @classmethod
    def getClasses(cls, globPattern, rootDir='.', filterers=[]):
        pyFiles = glob.glob(globPattern, root_dir=rootDir, recursive=True)
        classes = []
        for pyFile in pyFiles:
            modPath = [rootDir] if rootDir else []
            modPath.append(pyFile)
            try:
                modName = os.path.basename(join(*modPath))[:-3]
                spec = importlib.util.spec_from_file_location(modName, join(*modPath))
                mod = importlib.util.module_from_spec(spec)
                sys.modules[modName] = mod
                spec.loader.exec_module(mod)
                nameClassPairs = inspect.getmembers(mod, inspect.isclass)
                for name, aClass in nameClassPairs:
                    if not cls.isOwnModuleClass(mod, aClass):
                        continue
                    if R.find(lambda filterer: not filterer(name, aClass))(filterers):
                        continue
                    classes.append({
                        'path': join(*modPath),
                        'module': modPath[-1][:-3].replace('/', '.'),
                        'className': name,
                        'cls': aClass,
                    })
            except ModuleNotFoundError as e:
                print(e)
        return classes

    @classmethod
    def dumps(cls, thing):
        dumps(thing, cls=cls.JSONEncoder())

    @classmethod
    def JSONEncoder(cls):

        class _(cls):

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
