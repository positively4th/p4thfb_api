
from contrib.pyas.src.pyas_v3 import Leaf

from src.store.event.type.typestore import TypeStore
from src.mappers.tacticsmapper_v2 import TacticsMapper


class TacticsStore(Leaf):

    typeName = 'carry'
    Mapper = TacticsMapper

    prototypes = [TypeStore] + TypeStore.prototypes

    columnSpecs = {}
