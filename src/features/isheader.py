
from constants.statsbomb import StatsBomb as SB


class IsHeader:

    prototypes = []

    def _value(self, ttype):
        if ttype is None:
            self.addMetaKeyVal('Error', 'Type is missing.')
            return None

        if not 'bodyPartId' in ttype:
            self.addMetaKeyVal('Error', 'Body part is missing.')
            return None

        self.addMetaKeyVal(ttype['bodyPartId'], ttype['bodyPartName'])

        return int(ttype['bodyPartId'] in SB.headerBodyPartIds)

    @property
    async def value(self):
        raise Exception('Mot implemented.')
