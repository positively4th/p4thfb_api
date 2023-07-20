from quart import jsonify
import asyncio
import uvloop


def routes(app, appversion):

    assert isinstance(asyncio.new_event_loop(), uvloop.Loop)

    def version():
        assert isinstance(asyncio.new_event_loop(), uvloop.Loop)
        return jsonify({
            'version': [int(v) for v in appversion.split('.')]
        })

    async def config():
        assert isinstance(asyncio.new_event_loop(), uvloop.Loop)
        return jsonify({
            str(key): str(val) for key, val in app.config.items()
        })

    return {
        'config': (config, (), {'methods': ['GET']}),
        'version': (version, (), {'methods': ['GET']}),
    }
