import datetime
from quart import jsonify
from quart import request
import ramda as R

from contrib.pyas.src.pyas_v3 import As

from src.features.feature_v2 import Feature
from src.common.filter import Filter
from src.store.event.eventstore import EventStore
from src.plotters.plotter_v2 import Plotter
from src.mixins.classidentified import ClassIdentified
from src.mixins.config.config import Config
from src.store.autostores import getAutoStores


def routes(statDB, estimatorDB):

    stores = getAutoStores()

    async def plotter(plotterId):

        async def helper(resp) -> dict:
            payload = await request.json
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
                    filterers=[lambda name, cls: ClassIdentified.id(cls) in featureIds])
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

            eventStoree = As(EventStore)({**stores['eventStore']})
            filteree = As(Filter)(payload['eventFilter'])
            qp = Filter.eventFilter, {}
            qp = filteree.apply(statDB.createPipes(), qp)
            rows = await statDB.query(qp)
            ids = [r['__id'] for r in rows]
            events = R.unnest((await eventStoree.get(ids)).values())
            plotter.update({
                'eventIds': [e['event__id'] for e in events],
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

            plotNode = await As(PlotterClass)(plotter).plot(events)

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
        resp.update(await helper(resp))
        return jsonify(resp)

    return {
        '<plotterId>': (plotter, (), {'methods': ['PUT']}),
    }
