from contrib.pyas.src.pyas_v3 import Leaf

from src.store.store import Store
from src.mappers.visibleplayersmapper_v2 import VisiblePlayersMapper


class VisiblePlayersStore(Leaf):

    Mapper = VisiblePlayersMapper

    prototypes = [Store] + Store.prototypes

    columnSpecs = {}

    async def byEvent(self, event__id: str) -> list[str]:
        mapperee = self['mapperee']
        vps__ids = (await mapperee.event__id2__id(event__id))

        return await self.get(vps__ids[0]) if len(vps__ids) == 1 else None
