# import matplotlib
# matplotlib.use('qtagg')
# print(matplotlib.get_backend())
from threading import Lock
from flask import json
from flask_cors import CORS
from flask import Flask
import logging
from os import environ
import argparse

from contrib.p4thpydb.db.sqlite.db import DB as SQLITEDB
from contrib.p4thpydb.db.pgsql.db import DB as PGSQLDB

from src.tools.app import createConfigGetter
from src.tools.app import setupDBs
from src.tools.app import addRoute

from src.routes.matches import routes as matchRoutes
from src.routes.competitions import routes as competitionRoutes
from src.routes.events_v1 import routes as eventsRoutes
from routes.plotters_v1 import routes as plottersRoutes
from src.routes.plotter_v1 import routes as plotterRoutes
from routes.estimators_v1 import routes as estimatorsRoutes
from routes.estimator_v1 import routes as estimatorRoutes
from src.routes.features_v1 import routes as featuresRoutes
from routes.feature_v1 import routes as featureRoutes
from routes.system_v1 import routes as systemRoutes
from src.tools.python_v1 import Python
from src.mixins.versionguard import globalVersionGuard

applicationVersion = '0.0.0'

logging.basicConfig(level=logging.WARN)
apiLogger = logging.getLogger('api')

parser = argparse.ArgumentParser(description='p4thfb_api')
parser.add_argument('-c', metavar='configfile',
                    dest='CONFIGFILE', type=str, help='Path to config file.')
args = parser.parse_args()

app = Flask(__name__)
CORS(app)
app.json = Python.JSONProvider(app)
app.json.compact = True
app.json.sort_keys = False

configGetter = createConfigGetter(app, environ, args)
app.config.update(configGetter())

globalVersionGuard().setDomainVersionMap(json.loads(
    json.dumps({
        **app.config['DOMAINVERSIONMAP'],
        **{'application': applicationVersion},
    }))
)


statDB, estimatorDB, timeLogDB = setupDBs(PGSQLDB, SQLITEDB, configGetter)
assert statDB
assert timeLogDB

estimatorCacheLock = Lock()


for path, handler in matchRoutes(statDB).items():
    addRoute(app, '/matches/', path, handler, logger=apiLogger)
for path, handler in competitionRoutes(statDB).items():
    addRoute(app, '/competitions/', path, handler, logger=apiLogger)
for path, handler in eventsRoutes(statDB).items():
    addRoute(app, '/events/', path, handler, logger=apiLogger)
for path, handler in featuresRoutes(statDB).items():
    addRoute(app, '/features/', path, handler, logger=apiLogger)
for path, handler in featureRoutes(statDB).items():
    addRoute(app, '/feature/', path, handler, logger=apiLogger)
for path, handler in plottersRoutes().items():
    addRoute(app, '/plotters', path, handler, logger=apiLogger)
for path, handler in plotterRoutes(statDB, estimatorDB).items():
    addRoute(app, '/plotter', path, handler, logger=apiLogger)
for path, handler in estimatorRoutes(statDB, estimatorDB, estimatorCacheLock).items():
    addRoute(app, '/estimator/', path, handler, logger=apiLogger)
for path, handler in estimatorsRoutes(estimatorDB).items():
    addRoute(app, '/estimators/', path, handler, logger=apiLogger)
for path, handler in systemRoutes(app, applicationVersion).items():
    addRoute(app, '/system/', path, handler, logger=apiLogger)


if __name__ == '__main__':

    app.run(host=configGetter('HOST', '127.0.0.1'), port=configGetter(
        'PORT', 3000), debug=True, use_debugger=False, use_reloader=False)
