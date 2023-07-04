from flask import jsonify

from src.features.feature import Feature


def routes(db):

    def features():
        features = [dict(f) for f in Feature.getFeatures()]
        for feature in features:
            del feature['cls']
        return jsonify(features)

    return {
        '': features,
    }
