
from contrib.pyas.src.pyas_v3 import Leaf

from src.store.event.type.typestore import TypeStore
from src.mappers.interceptionmapper_v2 import InterceptionMapper


class InterceptionStore(Leaf):

    typeName = 'interception'
    Mapper = InterceptionMapper

    prototypes = [TypeStore] + TypeStore.prototypes

    columnSpecs = {}
