import ramda as R
from contrib.pyas.src.pyas_v3 import As

from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011
from mixins.event.event import Event
from src.tools.matcher import Matcher


class NOP:

    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    def _value(self, withinPossessionEvents):
        matchCondition = [
            Event.isPassEvent,
            '&',
            Event.isPossessionTeamEvent
        ]
        assert self.passesMin is not None or self.passesMax is not None

        events = withinPossessionEvents

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

    @property
    def value(self):
        raise Exception('Not implemented')
