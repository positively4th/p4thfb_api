from flask import jsonify
from flask import request
import importlib

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thcson.src.cson import cson

from src.features.feature import Feature


def routes(db):

    def feature(featureId):
        event = cson.fromJSON(request.data)
        feature = Feature.getFeatures(featureId=featureId)
        assert len(feature) == 1
        feature = feature[0]

        FeatureClass = getattr(importlib.import_module(
            feature['path']), feature['className'])
        FeatureClass = As(FeatureClass)
        feature = FeatureClass(event)
        return jsonify({
            'name': Feature.featureName(FeatureClass),
            'id': Feature.featureId(FeatureClass),
            'value': feature.value,
            'meta': feature.meta,
        })

    return {
        '/<featureId>': (feature, (), {'methods': ['POST']})
    }
