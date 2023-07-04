from quart import jsonify
from quart import request

from contrib.p4thcson.src.cson import cson

from src.features.feature_v2 import Feature


def routes(db):

    async def feature(featureId):
        event = cson.fromJSON(await request.data)
        feature = Feature.getFeatures(featureId=featureId)
        assert len(feature) == 1
        feature = feature[0]

        FeatureClass = feature['cls']
        feature = FeatureClass(event)
        return jsonify({
            'name': Feature.featureName(FeatureClass),
            'id': Feature.featureId(FeatureClass),
            'value': await feature.value,
            'meta': feature.meta,
        })

    return {
        '/<featureId>': (feature, (), {'methods': ['POST']})
    }
