from json import load
from collections.abc import Mapping
from logging import getLogger

from contrib.p4thpydb.db.pgsql.db import DB as PQSQLDB
from contrib.p4thpydb.db.pgsql.db_async import DB as PQSQLDBASYNC
from contrib.p4thpydb.db.sqlite.db import DB as SQLITEDB
from contrib.p4thpydb.db.sqlite.db_async import DB as SQLITEDBASYNC
from contrib.pyas.src.pyas_v3 import As


class App:

    @classmethod
    def createConfigGetter(cls, app, environ: Mapping, args, config: dict = {}):

        def configGetter(name=None, defVal=None, config=config):

            if name is None:
                return config

            res = None
            res = environ.get(name, None) if res is None else res
            res = getattr(args, name) if res is None and name in args else res
            res = config[name] if res is None and name in config else res
            res = defVal if res is None else res
            return res

        configFile = configGetter('CONFIGFILE', 'config.json')
        print('Loading conf from: ', configFile)

        config.update(dict(app.config))
        with open(configFile) as f:
            config.update(load(f))

        return configGetter

    @classmethod
    def createConnect2DB(cls):

        def connect2DB(dbConfig):
            asyncDB = 'ASYNC' in dbConfig and dbConfig['ASYNC']
            if dbConfig['TYPE'] == 'pgsql':
                return PQSQLDBASYNC(*dbConfig['args'], **dbConfig['kwargs']) if asyncDB else PQSQLDB(*dbConfig['args'], **dbConfig['kwargs'])
            if dbConfig['TYPE'] == 'sqlite':
                return SQLITEDBASYNC(*dbConfig['args'], **dbConfig['kwargs']) if asyncDB else SQLITEDB(*dbConfig['args'], **dbConfig['kwargs'])

            print('dbConfig', dbConfig)
            return None

        return connect2DB

    @classmethod
    def setupDBs(cls, configGetter):

        connect2DB = cls.createConnect2DB()
        return (
            connect2DB(configGetter('STATDB')),
            lambda: connect2DB(configGetter('ESTIMATORDB')),
            connect2DB(configGetter('TIMELOGDB'))
        )

    @classmethod
    def addRoute(cls, app, prefix: str, path: str, handler: dict, logger: None):

        _logger = getLogger() if logger is None else logger

        def joinIf(parts, sep):
            return sep.join([
                part for part in parts if part != ''
            ])

        fullPath = joinIf([
            prefix.rstrip('/'),
            path.strip('/'),
        ], '/')
        kwArgs = {**{'strict_slashes': False}, **handler[2]}
        app.route(fullPath, *handler[1], **kwArgs)(handler[0])
        _logger.info('Added route %s.', fullPath)
