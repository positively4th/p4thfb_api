import json
from quart import jsonify
from quart import request
import ramda as R

from contrib.pyas.src.pyas_v3 import As

from src.common.filter import Filter
from src.tools.python_v2 import Python
from src.store.event.eventstore import EventStore
from src.mixins.event.event_v2 import Event
from src.mixins.contextlogger import ContextLogger
from src.store.autostores import getAutoStores


def routes(db, timeLogDB):

    stores = getAutoStores()

    oneLevelExportFeatures = {
        'relatedEvents': None,
        'visiblePlayers': None,
        'visibleArea': None,
        'type': None,
    }

    async def eventsHandler():

        eventStoree = As(EventStore)({**stores['eventStore']})
        filter = request.args.get('filter')
        filter = json.loads(filter) if filter is not None else {}
        filteree = As(Filter)({} if filter is None else filter)

        qp = Filter.eventFilter, {}
        qp = filteree.apply(db.createPipes(), qp)

        rows = await ContextLogger.asLogged(db.query,
                                            resultHandler=ContextLogger.countResultHandler,
                                            )(qp)

        ids = [r['__id'] for r in rows]

        events = await ContextLogger.asLogged(eventStoree.get,
                                              resultHandler=ContextLogger.countResultHandler,
                                              )(ids)

        events = await ContextLogger.asLogged(Event.export,
                                              resultHandler=ContextLogger.countResultHandler,
                                              )(R.unnest(events.values()),
                                                features={
                                                  'relatedEvents': {**oneLevelExportFeatures},
                                                  # 'relatedEvents': {},
                                                  'visiblePlayers': None,
                                                  'visibleArea': None,
                                                  'type': None,
                                              },
        )

        resp = ContextLogger.asLogged(Python.CSONWrapper)(events)

        resp = ContextLogger.asLogged(jsonify)(resp)
        return resp

    return {
        '/': (eventsHandler, (), {'methods': ['GET']}),
    }
