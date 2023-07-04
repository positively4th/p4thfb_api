import ramda as R
from matplotlib import pyplot as plt

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.estimators.mixins.estimationnode import EstimationNode


class PlotterError(Exception):
    pass


class Plotter(Leaf):

    prototypes = []

    columnSpecs = {
        'estimator': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }

    def _plot(self, estimationNode, plotName, args=[], argMap={}):
        raise PlotterError('Not implemented.')

    def plotter(self, estimationNode, plotName, args=[], argMap={}, estimationNodeId=None):
        res = R.pick(['estimatorId', 'jiff', 'id'])(
            {
                **estimationNode,
                **{'plotName': plotName, 'args': args, 'argMap': argMap},
            })

        branches = estimationNode['estimationNodes'] if 'estimationNodes' in estimationNode else [
        ]

        doPlot = 'results' in estimationNode \
            and (
                estimationNodeId is None
                or
                estimationNodeId == As(EstimationNode)(estimationNode)['id']
            )

        if len(branches) == 0:
            res['plots'] = As(EstimationNode).Skip

        if doPlot:
            res['plot'] = self._plot(
                estimationNode, plotName, args=args, argMap=argMap)
            res['plots'] = As(EstimationNode).Skip

        return res
