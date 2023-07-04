
from contrib.pyas.src.pyas_v3 import T

from src.store.store import Store


class TypeStore():

    prototypes = [Store] + Store.prototypes

    columnSpecs = {}

    async def byEvent(self, event__id: str | list[str]):
        mapperee = self['mapperee']
        pass__id = (await mapperee.event__id2__id(event__id))[0]
        return (await self.get(pass__id))[0]
