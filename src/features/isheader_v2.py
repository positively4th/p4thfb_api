
from contrib.pyas.src.pyas_v3 import Leaf

from constants.statsbomb import StatsBomb as SB
from src.features.feature_v2 import Feature


class IsHeader(Leaf):

    prototypes = [Feature]

    def __init__(self, event, *args, **kwargs):
        super().__init__(event, *args, **kwargs)

    @property
    async def value(self):
        eventee = self.eventee

        ttype = await eventee['type']
        if ttype is None:
            self.addMetaKeyVal('Error', 'Type is missing.')
            return None

        if not 'bodyPartId' in ttype:
            self.addMetaKeyVal('Error', 'Body part is missing.')
            return None

        self.addMetaKeyVal(ttype['bodyPartId'], ttype['bodyPartName'])

        return int(ttype['bodyPartId'] in SB.headerBodyPartIds)
