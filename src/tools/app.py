from json import load
from collections.abc import Mapping
from logging import getLogger

def createConfigGetter(app, environ: Mapping, args, config : dict={}):


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


def createConnect2DB(PGDB, SqliteDB):

    def connect2DB(dbConfig):
        if dbConfig['TYPE'] == 'pgsql':
            return PGDB(*dbConfig['args'], **dbConfig['kwargs'])
        if dbConfig['TYPE'] == 'sqlite':
            return SqliteDB(*dbConfig['args'], **dbConfig['kwargs'])

        print('dbConfig', dbConfig)
        return None

    return connect2DB

def setupDBs(PGDB, SqliteDB, configGetter):

    connect2DB = createConnect2DB(PGDB, SqliteDB)
    return (
        connect2DB(configGetter('STATDB')),
        lambda: connect2DB(configGetter('ESTIMATORDB')),
            connect2DB(configGetter('TIMELOGDB'))
    )


def addRoute(app, prefix: str, path: str, handler: dict, logger: None):

    _logger = getLogger() if logger is None else logger

    def joinIf(parts, sep):
        return sep.join([
            part for part in parts if part != ''
        ])

    fullPath = joinIf([
        prefix.rstrip('/'), 
        path.strip('/'),
    ], '/')
    kwArgs = { **{ 'strict_slashes': False }, **handler[2] }
    app.route(fullPath, *handler[1], **kwArgs)(handler[0])
    _logger.info('Added route %s.', fullPath)
