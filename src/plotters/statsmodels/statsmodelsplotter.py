
from src.plotters.plotter import Plotter


class StatsmodelsPlotter:

    prototypes = [Plotter] + Plotter.prototypes

    columnSpecs = {}

    @classmethod
    def onNew(cls, self):
        pass
