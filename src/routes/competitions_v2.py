from quart import jsonify

from contrib.pyas.src.pyas_v3 import As

from src.mappers.competition.competitionmapper import CompetitionMapper


def routes(db):

    async def competitions():
        rows = As(CompetitionMapper)({}).load(db)
        return jsonify({
            'result': [r for r in rows]
        })

    return {
        '': (competitions, (), {'methods': ['GET']}),
    }
