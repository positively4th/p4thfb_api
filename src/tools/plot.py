import io
import base64

from colour import Color as Colour
from matplotlib.figure import Figure


class Plot:

    @staticmethod
    def plotAsBase64(plt):
        # plt.show()

        bbytes = io.BytesIO()

        plt.savefig(bbytes, format='png')
        bbytes.seek(0)
        return base64.b64encode(bbytes.read()).decode('ascii')

    @classmethod
    def asJSON(cls, plt):

        if not isinstance(plt, Figure):
            return plt

        return {
            'transforms': ['png', 'base64'],
            'data': cls.plotAsBase64(plt)
        }
