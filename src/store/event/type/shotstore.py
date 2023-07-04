
from contrib.pyas.src.pyas_v3 import Leaf

from src.store.event.type.typestore import TypeStore
from src.mappers.shotmapper_v2 import ShotMapper


class ShotStore(Leaf):

    typeName = 'shot'
    Mapper = ShotMapper

    prototypes = [TypeStore] + TypeStore.prototypes

    columnSpecs = {}
