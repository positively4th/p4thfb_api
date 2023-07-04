from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v2 import Feature
from src.mappers.event.constants import Constants


class StatsBombXG(Leaf):

    prototypes = [Feature] + Feature.prototypes

    @property
    async def value(self):

        if self.eventee['typeId'] != Constants.shotTypeId:
            self.addMetaKeyVal('Error', 'Wrong event type: {}'.format(
                self.eventee['typeName']))
            return float('nan')
        _type = await self.eventee['type']
        if _type is None:
            self.addMetaKeyVal('Error', 'Event is missing shot data.')
            return float('nan')
        xG = float(_type['xG'])
        if xG == xG and xG != float('inf') and xG != float('-inf'):
            return xG

        self.addMetaKeyVal(
            'Error', 'Event xG {} is not a number.'.format(self.eventee.xG))
        return float('nan')
