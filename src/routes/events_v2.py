import json
from quart import jsonify
from quart import request
import ramda as R
import datetime

from contrib.pyas.src.pyas_v3 import As

from src.common.filter import Filter
from src.tools.python_v2 import Python
from src.store.event.eventstore import EventStore
from src.mixins.event.event_v2 import Event
from src.mixins.timelogdb import TimeLogDB
from src.store.autostores import getAutoStores


def routes(db, timeLogDB):

    timeLogDBee = As(TimeLogDB)({
        'timeLogDB': timeLogDB
    })

    stores = getAutoStores()

    oneLevelExportFeatures = {
        'relatedEvents': None,
        'visiblePlayers': None,
        'visibleArea': None,
        'type': None,
    }

    async def events():

        group = datetime.datetime.now().isoformat()

        eventStoree = As(EventStore)({**stores['eventStore']})
        filter = request.args.get('filter')
        filter = json.loads(filter) if filter is not None else {}
        filteree = As(Filter)({} if filter is None else filter)

        qp = Filter.eventFilter, {}
        qp = filteree.apply(db.createPipes(), qp)
        rows = await db.query(qp)
        ids = [r['__id'] for r in rows]
        events = await (timeLogDBee.asRuntimeLogged(eventStoree.get,
                                                    identifier=__file__,
                                                    tag='eventStoree.get',
                                                    group=group,
                                                    count=len(ids)))(ids)
        events = await (timeLogDBee.asRuntimeLogged(Event.export,
                                                    identifier=__file__,
                                                    tag='Event.export',
                                                    group=group,
                                                    count=len(ids)))(R.unnest(events.values()), features={
                                                        'relatedEvents': {**oneLevelExportFeatures},
                                                        'visiblePlayers': None,
                                                        'visibleArea': None,
                                                        'type': None,
                                                    })

        resp = await (timeLogDBee.asRuntimeLogged(jsonify, identifier=__file__,
                                                  tag='jsonify',
                                                  group=group,
                                                  count=len(ids)))(Python.CSONWrapper(events))
        return resp

    return {
        '/': (events, (), {'methods': ['GET']}),
    }
