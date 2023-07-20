from flask import jsonify
from flask import request
import importlib

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thcson.src.cson import cson

from src.features.feature_v1 import Feature


def routes(db):

    def feature(featureId):
        event = cson.fromJSON(request.data)
        feature = As(Feature).getFeatures(featureId=featureId)
        assert len(feature) == 1
        feature = feature[0]

        FeatureClass = importlib.import_module(feature['module'])
        FeatureClass = getattr(FeatureClass, feature['className'])
        FeatureClass = As(FeatureClass)
        feature = FeatureClass(event)
        return jsonify({
            'name': FeatureClass.featureName(FeatureClass),
            'id': FeatureClass.featureId(FeatureClass),
            'value': feature.value,
            'meta': feature.meta,
        })

    return {
        '/<featureId>': (feature, (), {'methods': ['POST']})
    }
