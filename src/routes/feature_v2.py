from quart import jsonify
from quart import request

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thcson.src.cson import cson

from src.features.feature_v2 import Feature


def routes(db):

    async def feature(featureId):
        event = cson.fromJSON(await request.data)
        feature = As(Feature).getFeatures(featureId=featureId)
        assert len(feature) == 1
        feature = feature[0]

        FeatureClass = feature['cls']
        feature = FeatureClass(event)
        return jsonify({
            'name': As(Feature).featureName(FeatureClass),
            'id': As(Feature).featureId(FeatureClass),
            'value': await feature.value,
            'meta': feature.meta,
        })

    return {
        '/<featureId>': (feature, (), {'methods': ['POST']})
    }
