from quart import jsonify

from contrib.pyas.src.pyas_v3 import As

from src.plotters.plotter_v2 import Plotter
from src.mixins.classidentified import ClassIdentified


def routes():

    _allPlotters = None

    def getAllPlotters():

        nonlocal _allPlotters

        if _allPlotters is None:
            _allPlotters = Plotter.getPlotters()
            for p in _allPlotters:
                p['id'] = ClassIdentified.id(As(p['cls']))
                del p['cls']
                del p['path']
                del p['className']
        return _allPlotters

    def plotters():

        return jsonify(getAllPlotters())

    return {
        '': (plotters, (), {'methods': ['GET']}),
    }
