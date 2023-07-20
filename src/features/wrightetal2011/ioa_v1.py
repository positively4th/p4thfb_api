from contrib.pyas.src.pyas_v3 import Leaf

from src.features.feature_v1 import Feature
from features.wrightetal2011.ioa import IOA as IOA0


class IOA:

    prototypes = [
        IOA0, *IOA0.prototypes,
        Feature, *Feature.prototypes,
    ]

    @property
    def value(self):
        return self._value(self.event['relatedEvents'])


class IOAFreeKick(Leaf):
    prototypes = [IOA] + IOA.prototypes


class IOACorner(Leaf):
    prototypes = [IOA] + IOA.prototypes


class IOAThrowIn(Leaf):
    prototypes = [IOA] + IOA.prototypes


class IOAInterception(Leaf):
    prototypes = [IOA] + IOA.prototypes


class IOASuccessfulTackle(Leaf):
    prototypes = [IOA] + IOA.prototypes


class IOAOther(Leaf):
    prototypes = [IOA] + IOA.prototypes


class IOAGoalKick(Leaf):
    prototypes = [IOA] + IOA.prototypes


class IOAKickOff(Leaf):
    prototypes = [IOA] + IOA.prototypes


class IOAPenalty(Leaf):
    prototypes = [IOA] + IOA.prototypes
