from flask import jsonify


def routes(app, appversion):

    def version():
        return jsonify({
            'version': [int(v) for v in appversion.split('.')]
        })

    def config():
        return jsonify({
            str(key): str(val) for key, val in app.config.items()
        })

    return {
        'config': (config, (), {'methods': ['GET']}),
        'version': (version, (), {'methods': ['GET']}),
    }
