from flask import jsonify

from contrib.pyas.src.pyas_v3 import As
from src.features.feature_v1 import Feature


def routes(db):

    def features():
        features = [dict(f) for f in As(Feature).getFeatures()]
        for feature in features:
            del feature['cls']
        return jsonify(features)

    return {
        '/': (features, (), {'methods': ['GET']}),
    }
