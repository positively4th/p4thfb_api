from src.plotters.plotter_v2 import Plotter


class StatsmodelsPlotter:

    prototypes = [Plotter] + Plotter.prototypes

    columnSpecs = {}

    @classmethod
    def onNew(cls, self):
        pass
