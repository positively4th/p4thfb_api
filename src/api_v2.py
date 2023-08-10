# import matplotlib
# matplotlib.use('qtagg')
# print(matplotlib.get_backend())
from quart_cors import cors
from quart import Quart
import argparse
from os import environ
import logging
import json
import asyncio
import uvloop

from contrib.pyas.src.pyas_v3 import As

from src.mixins.versionguard import globalVersionGuard
from src.tools.python_v2 import Python
from src.routes.system_v2 import routes as systemRoutes
from src.routes.feature_v2 import routes as featureRoutes
from src.routes.features_v2 import routes as featuresRoutes
from src.routes.estimator_v2 import routes as estimatorRoutes
from src.routes.estimators_v2 import routes as estimatorsRoutes
from src.routes.plotters_v2 import routes as plottersRoutes
from src.routes.plotter_v2 import routes as plotterRoutes
from src.routes.events_v2 import routes as eventsRoutes
from src.routes.competitions_v2 import routes as competitionRoutes
from src.routes.matches_v2 import routes as matchRoutes
from src.store.autostores import setAutoStoresDBs
from src.tools.app_v2 import App
from src.mixins.contextlogger import ContextLogger

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# assert isinstance(asyncio.new_event_loop(), uvloop.Loop)
applicationVersion = '1.0.0'

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)
apiLogger = logging.getLogger('api')

parser = argparse.ArgumentParser(description='p4thfb_api_v2')
parser.add_argument('-c', metavar='configfile',
                    dest='CONFIGFILE', type=str, help='Path to config file.')
parser.add_argument('-d', action='store_true',
                    dest='DEBUG', help='Run in debug mode')
args = parser.parse_args()

app = Quart(__name__)
app = cors(app, allow_origin="*")
app.json = Python.JSONProvider(app)
app.json.compact = True
app.json.sort_keys = False

configGetter = App.createConfigGetter(app, environ, args)
app.config.update(configGetter())

globalVersionGuard().setDomainVersionMap(
    json.loads(
        json.dumps({
            **app.config['DOMAINVERSIONMAP'],
            **{'application': applicationVersion},
        }))
)

statDB, estimatorDB, timeLogDB = App.setupDBs(configGetter)
assert statDB
assert timeLogDB

setAutoStoresDBs(statDB)
ContextLogger.setContextLogger(As(ContextLogger)({
    'timeLogDB': timeLogDB,
    'isActive': not configGetter('DEBUG'),
    'staticData': {
        'identifier': 'p4thfb_api',
        'tag': 'api_v2',
        'traceId': '',
        'queryString': '',
        'count': 1,

    }
}))

for path, handler in matchRoutes(statDB).items():
    App.addRoute(app, '/matches/', path, handler,
                 logger=apiLogger, timelogDB=timeLogDB)
for path, handler in competitionRoutes(statDB).items():
    App.addRoute(app, '/competitions/', path, handler,
                 logger=apiLogger, timelogDB=timeLogDB)
for name, handler in eventsRoutes(statDB, timeLogDB).items():
    App.addRoute(app, '/events/', name, handler,
                 logger=apiLogger, timelogDB=timeLogDB)
for name, handler in featuresRoutes(statDB).items():
    App.addRoute(app, '/features/', name, handler,
                 logger=apiLogger, timelogDB=timeLogDB)
for path, handler in featureRoutes(statDB).items():
    App.addRoute(app, '/feature/', path, handler,
                 logger=apiLogger, timelogDB=timeLogDB)
for path, handler in plotterRoutes(statDB, estimatorDB).items():
    App.addRoute(app, '/plotter', path, handler,
                 logger=apiLogger, timelogDB=timeLogDB)
for path, handler in plottersRoutes().items():
    App.addRoute(app, '/plotters', path, handler,
                 logger=apiLogger, timelogDB=timeLogDB)
for path, handler in estimatorRoutes(statDB, estimatorDB).items():
    App.addRoute(app, '/estimator/', path, handler,
                 logger=apiLogger, timelogDB=timeLogDB)
for path, handler in estimatorsRoutes(estimatorDB).items():
    App.addRoute(app, '/estimators/', path, handler,
                 logger=apiLogger, timelogDB=timeLogDB)
for path, handler in systemRoutes(app, applicationVersion).items():
    App.addRoute(app, '/system/', path, handler,
                 logger=apiLogger, timelogDB=timeLogDB)


if __name__ == '__main__':
    debug = configGetter('DEBUG', False)
    app.run(loop=asyncio.get_event_loop(), host=configGetter('HOST', '127.0.0.1'), port=configGetter('PORT', 3000), debug=debug,
            use_debugger=False, use_reloader=False)
