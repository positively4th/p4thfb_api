from contrib.pyas.src.pyas_v3 import Leaf

from src.store.store import Store
from src.mappers.visibleareamapper_v2 import VisibleAreaMapper


class VisibleAreaStore(Leaf):

    Mapper = VisibleAreaMapper

    prototypes = [Store] + Store.prototypes

    columnSpecs = {}

    async def byEvent(self, event__id: str) -> list[str]:
        mapperee = self['mapperee']
        va__ids = (await mapperee.event__id2__id(event__id))
        return await self.get(va__ids[0]) if len(va__ids) == 1 else None
