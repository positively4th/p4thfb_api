from src.mappers.event.constants import Constants


class StatsBombXG:

    prototypes = []

    def _value(self, _type):

        if self.eventee['typeId'] != Constants.shotTypeId:
            self.addMetaKeyVal('Error', 'Wrong event type: {}'.format(
                self.eventee['typeName']))
            return float('nan')

        if _type is None:
            self.addMetaKeyVal('Error', 'Event is missing shot data.')
            return float('nan')
        xG = float(_type['xG'])
        if xG == xG and xG != float('inf') and xG != float('-inf'):
            return xG

        self.addMetaKeyVal(
            'Error', 'Event xG {} is not a number.'.format(self.eventee.xG))
        return float('nan')
