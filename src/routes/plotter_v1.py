import datetime
from flask import jsonify
from flask import request

from contrib.pyas.src.pyas_v3 import As

from src.features.feature_v1 import Feature
from src.common.filter import Filter
from src.mappers.event.eventmapper import EventMapper
from src.plotters.plotter_v1 import Plotter
from src.mixins.classidentified import ClassIdentified

from src.mixins.config.config import Config


def routes(statDB, estimatorDB):

    def plotter(plotterId):

        def helper(resp) -> dict:
            payload = request.json
            featureIds = payload['featureIds']
            config = payload['config'] if 'config' in payload else None

            PlotterClass = [
                spec['cls'] for spec in As(Plotter).getPlotters([
                    lambda name, cls: ClassIdentified.id(
                        As(cls)) == plotterId
                ])
            ]
            assert 1 == len(PlotterClass)
            PlotterClass = PlotterClass[0]
            plotter = {
                'jiff': datetime.datetime.now(),
                'estimatorId': plotterId,
                'eventIds': [],
                'state': 'running',
                'error': '',
            }

            allFeatureClasses = As(Feature).allFeaturesClasses()

            FeatureClasses = [
                spec['cls'] for spec in As(Feature).getFeatures(
                    filterers=[
                        lambda name, cls: ClassIdentified.id(cls) in featureIds]
                )
            ]
            plotter.update({
                'FeatureClasses': FeatureClasses,
            })

            config = As(PlotterClass)(plotter).updateConfig(
                config, allFeatureClasses=allFeatureClasses,
                selectedFeatureClasses=FeatureClasses)
            configee = As(Config)(config)
            if not configee.evaluate():
                return {
                    'config': config,
                    'hasError': True,
                }

            filteree = As(Filter)(payload['eventFilter'])
            pq = Filter.eventFilter, {}
            pq = filteree.apply(statDB.createPipes(), pq)
            events = As(EventMapper)({}).load(statDB, pq)
            plotter.update({
                'eventIds': [e['__id'] for e in events],
            })

            As(PlotterClass)(plotter).updateConfig(
                config, allFeatureClasses=As(Feature).allFeaturesClasses(),
                selectedFeatureClasses=FeatureClasses,
                events=events)
            if not configee.evaluate():
                return {
                    'config': config,
                    'hasError': True,
                }

            plotNode = As(PlotterClass)(plotter).plot(events)

            return {
                'plotNode': plotNode,
                'config': config,
                'hasError': False,
            }

        resp = {
            'plotNode': None,
            'config': None,
            'hasError': False,

        }
        resp.update(helper(resp))
        return jsonify(resp)

    return {
        '<plotterId>': (plotter, (), {'methods': ['PUT']}),
    }
