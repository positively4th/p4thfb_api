from quart import jsonify
from quart import request
import json

from contrib.pyas.src.pyas_v3 import As

from src.mappers.match.matchmapper import MatchMapper


def routes(db):

    async def matches():
        filter = request.args.get('filter')
        filter = json.loads(filter) if filter is not None else {}

        rows = As(MatchMapper)({}).load(db, filter=filter)
        return jsonify({
            'result': [r for r in rows]
        })

    return {
        '': matches
    }
