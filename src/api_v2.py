# import matplotlib
# matplotlib.use('qtagg')
# print(matplotlib.get_backend())

import json

from quart import Quart
from quart_cors import cors

from contrib.p4thpydb.db.sqlite.db_async import DB as SQLITEDB
from contrib.p4thpydb.db.pgsql.db_async import DB as PGSQLDB

from src.store.autostores import setAutoStoresDBs
from src.routes.matches_v2 import routes as matchRoutes
from src.routes.competitions_v2 import routes as competitionRoutes
from src.routes.events_v2 import routes as eventsRoutes
from src.routes.plotter_v2 import routes as plotterRoutes
from src.routes.plotters_v2 import routes as plottersRoutes
from src.routes.estimators_v2 import routes as estimatorsRoutes
from src.routes.estimator_v2 import routes as estimatorRoutes
from src.routes.features_v2 import routes as featuresRoutes
from src.routes.feature_v2 import routes as featureRoutes
from src.routes.system_v2 import routes as systemRoutes
from src.tools.python_v2 import _JSONProvider
from src.mixins.versionguard import globalVersionGuard

# logging.getLogger().setLevel(logging.INFO)


def connect2DB(dbConfig):
    if dbConfig['TYPE'] == 'pgsql':
        return PGSQLDB(*dbConfig['args'], **dbConfig['kwargs'])
    if dbConfig['TYPE'] == 'sqlite':
        return SQLITEDB(*dbConfig['args'], **dbConfig['kwargs'])

    print('dbConfig', dbConfig)
    return None


applicationVersion = '1.0.0'

app = Quart(__name__)
app = cors(app, allow_origin="*")
app.json = _JSONProvider(app)
app.json.compact = True
app.json.sort_keys = False

app.config.from_file("../config.json", load=json.load)

globalVersionGuard().setDomainVersionMap(
    json.loads(
        json.dumps({
            **app.config['DOMAINVERSIONMAP'],
            **{'application': applicationVersion},
        }))
)

statDB = connect2DB(app.config['STATDB'])
assert statDB
timeLogDB = connect2DB(app.config['TIMELOGDB'])
assert timeLogDB
def estimatorDB(): return connect2DB(app.config['ESTIMATORDB'])


setAutoStoresDBs(statDB, timeLogDB)


def addRoute(prefix: str, path: str, handler: dict):
    fullPath = '{}/{}'.format(prefix.rstrip('/'), path.lstrip('/'))
    app.route(fullPath, *handler[1], **handler[2])(handler[0])


for name, handler in matchRoutes(statDB).items():
    app.route('/matches/' + name)(handler)
for path, handler in competitionRoutes(statDB).items():
    addRoute('/competitions/', path, handler)
for name, handler in eventsRoutes(statDB, timeLogDB).items():
    app.route('/events/' + name)(handler)
for name, handler in featuresRoutes(statDB).items():
    app.route('/features/' + name)(handler)
for path, handler in featureRoutes(statDB).items():
    addRoute('/feature/', path, handler)
for path, handler in plotterRoutes(statDB, estimatorDB).items():
    addRoute('/plotter', path, handler)
for path, handler in plottersRoutes().items():
    addRoute('/plotters', path, handler)
for path, handler in estimatorRoutes(statDB, estimatorDB).items():
    addRoute('/estimator/', path, handler)
for path, handler in estimatorsRoutes(estimatorDB).items():
    addRoute('/estimators/', path, handler)
for path, handler in systemRoutes(app, applicationVersion).items():
    addRoute('/system/', path, handler)


if __name__ == '__main__':

    app.run(port=3000, debug=True, use_debugger=False, use_reloader=False)
