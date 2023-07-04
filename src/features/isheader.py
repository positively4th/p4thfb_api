from contrib.pyas.src.pyas_v3 import Leaf

from constants.statsbomb import StatsBomb as SB
from src.features.feature import Feature


class IsHeader(Leaf):

    prototypes = [Feature] + Feature.prototypes

    # @classmethod
    # def featureName(cls):
    #    return 'IsHeader';

    def __init__(self, event, *args, **kwargs):
        super().__init__(event, *args, **kwargs)

    @property
    def value(self):
        eventee = self.eventee

        if not 'type' in eventee:
            self.addMetaKeyVal('Error', 'Type is missing.')
            return None

        ttype = eventee['type']

        if not 'bodyPartId' in ttype:
            self.addMetaKeyVal('Error', 'Body part is missing.')
            return None

        self.addMetaKeyVal(ttype['bodyPartId'], ttype['bodyPartName'])

        return int(ttype['bodyPartId'] in SB.headerBodyPartIds)
