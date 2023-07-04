
from contrib.pyas.src.pyas_v3 import Leaf

from src.store.event.type.typestore import TypeStore
from src.mappers.clearancemapper_v2 import ClearnaceMapper


class ClearnaceStore(Leaf):

    typeName = 'clearance'
    Mapper = ClearnaceMapper

    prototypes = [TypeStore] + TypeStore.prototypes

    columnSpecs = {}
