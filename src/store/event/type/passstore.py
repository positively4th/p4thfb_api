
from contrib.pyas.src.pyas_v3 import Leaf

from src.store.event.type.typestore import TypeStore
from src.mappers.passmapper_v2 import PassMapper


class PassStore(Leaf):

    typeName = 'pass'
    Mapper = PassMapper

    prototypes = [TypeStore] + TypeStore.prototypes

    columnSpecs = {}
