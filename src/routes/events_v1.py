import json
from flask import jsonify
from flask import request

from contrib.pyas.src.pyas_v3 import As

from src.common.filter import Filter
from src.mappers.event.eventmapper import EventMapper
from src.tools.python_v1 import Python


def routes(db):

    def events():
        filter = request.args.get('filter')
        filter = json.loads(filter) if filter is not None else {}
        filteree = As(Filter)({} if filter is None else filter)

        qp = Filter.eventFilter, {}
        qp = filteree.apply(db.createPipes(), qp)

        events = As(EventMapper)({}).load(db, qp)
        return jsonify(Python.CSONWrapper(events))

    return {
        '/': (events, (), {'methods': ['GET']}),
    }
