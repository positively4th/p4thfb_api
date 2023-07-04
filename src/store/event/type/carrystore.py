
from contrib.pyas.src.pyas_v3 import Leaf

from src.store.event.type.typestore import TypeStore
from src.mappers.carrymapper_v2 import CarryMapper


class CarryStore(Leaf):

    typeName = 'carry'
    Mapper = CarryMapper

    prototypes = [TypeStore] + TypeStore.prototypes

    columnSpecs = {}
