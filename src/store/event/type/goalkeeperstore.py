
from contrib.pyas.src.pyas_v3 import Leaf

from src.store.event.type.typestore import TypeStore
from src.mappers.goalkeepermapper_v2 import GoalKeeperMapper


class GoalKeeperStore(Leaf):

    typeName = 'goalkeeper'

    Mapper = GoalKeeperMapper

    prototypes = [TypeStore] + TypeStore.prototypes

    columnSpecs = {}
