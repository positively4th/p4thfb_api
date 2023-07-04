import ramda as R
from os.path import dirname
from os.path import sep as pathsep
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011
from mixins.event.event import Event

from src.tools.matcher import Matcher


class NOP:

    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    @property
    def value(self):
        matchCondition = [
            Event.isPassEvent,
            '&',
            Event.isPossessionTeamEvent
        ]
        assert self.passesMin is not None or self.passesMax is not None

        eventee = As(Event)(self.event)
        events = eventee.withinPossessionEvents

        ownPassEvents = R.filter(
            lambda event: Matcher.isMatch(As(Event)(event), matchCondition)
        )(events)

        ownPassCount = len(ownPassEvents)
        self.addMetaKeyVal('passCount', str(ownPassCount))

        if self.passesMin is not None and ownPassCount < self.passesMin:
            return 0
        if self.passesMax is not None and ownPassCount > self.passesMax:
            return 0
        return 1


class NOP1to4(Leaf):
    prototypes = [NOP] + NOP.prototypes
    passesMin = 1
    passesMax = 4


class NOP5to8(Leaf):
    prototypes = [NOP] + NOP.prototypes
    passesMin = 5
    passesMax = 8


class NOP9toInfinity(Leaf):
    prototypes = [NOP] + NOP.prototypes
    passesMin = 9
    passesMax = None
