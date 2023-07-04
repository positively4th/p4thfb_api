
from contrib.pyas.src.pyas_v3 import Leaf

from src.store.event.type.typestore import TypeStore
from src.mappers.duelmapper_v2 import DuelMapper


class DuelStore(Leaf):

    typeName = 'duel'
    Mapper = DuelMapper

    prototypes = [TypeStore] + TypeStore.prototypes

    columnSpecs = {}
