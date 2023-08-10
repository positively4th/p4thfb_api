from src.mixins.versionguard import globalVersionGuard
from src.tools.python_v1 import Python
from routes.system_v1 import routes as systemRoutes
from routes.feature_v1 import routes as featureRoutes
from src.routes.features_v1 import routes as featuresRoutes
from routes.estimator_v1 import routes as estimatorRoutes
from routes.estimators_v1 import routes as estimatorsRoutes
from src.routes.plotter_v1 import routes as plotterRoutes
from routes.plotters_v1 import routes as plottersRoutes
from src.routes.events_v1 import routes as eventsRoutes
from src.routes.competitions import routes as competitionRoutes
from src.routes.matches import routes as matchRoutes
from src.tools.app import App
import argparse
from os import environ
import logging
from flask import Flask
from flask_cors import CORS
from flask import json
from threading import Lock
import matplotlib
matplotlib.use('agg')
# print(matplotlib.get_backend())


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

configGetter = App.createConfigGetter(app, environ, args)
app.config.update(configGetter())

globalVersionGuard().setDomainVersionMap(json.loads(
    json.dumps({
        **app.config['DOMAINVERSIONMAP'],
        **{'application': applicationVersion},
    }))
)


statDB, estimatorDB, timeLogDB = App.setupDBs(configGetter)
assert statDB
assert timeLogDB

estimatorCacheLock = Lock()


for path, handler in matchRoutes(statDB).items():
    App.addRoute(app, '/matches/', path, handler, logger=apiLogger)
for path, handler in competitionRoutes(statDB).items():
    App.addRoute(app, '/competitions/', path, handler, logger=apiLogger)
for path, handler in eventsRoutes(statDB).items():
    App.addRoute(app, '/events/', path, handler, logger=apiLogger)
for path, handler in featuresRoutes(statDB).items():
    App.addRoute(app, '/features/', path, handler, logger=apiLogger)
for path, handler in featureRoutes(statDB).items():
    App.addRoute(app, '/feature/', path, handler, logger=apiLogger)
for path, handler in plottersRoutes().items():
    App.addRoute(app, '/plotters', path, handler, logger=apiLogger)
for path, handler in plotterRoutes(statDB, estimatorDB).items():
    App.addRoute(app, '/plotter', path, handler, logger=apiLogger)
for path, handler in estimatorRoutes(statDB, estimatorDB, estimatorCacheLock).items():
    App.addRoute(app, '/estimator/', path, handler, logger=apiLogger)
for path, handler in estimatorsRoutes(estimatorDB).items():
    App.addRoute(app, '/estimators/', path, handler, logger=apiLogger)
for path, handler in systemRoutes(app, applicationVersion).items():
    App.addRoute(app, '/system/', path, handler, logger=apiLogger)


if __name__ == '__main__':

    app.run(host=configGetter('HOST', '127.0.0.1'), port=configGetter(
        'PORT', 3000), debug=True, use_debugger=False, use_reloader=False)
