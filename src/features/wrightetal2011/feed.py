import ramda as R

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.tools.matcher import Matcher
from mixins.event.event import Event


class Feed(Leaf):

    prototypes = []

    columnSpecs = {
        'index': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
        'relatedEvents': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }

    toEventMatcher = [
        Event.isPossessionTeamEvent,
        '&',
        [
            Event.isDribbleEvent,
            '|',
            Event.isCarryEvent,
        ]
    ]

    toEventIgnoreMatcher = [
        ['!', Event.isPossessionTeamEvent],
        '|',
        Event.isDribbledPastEvent,
    ]

    fromEventIgnoreMatcher = [
        ['!', Event.isPossessionTeamEvent],
        '|',
        Event.isBallReceiptEvent,
        '|',
        Event.isBadBehaviourEvent,
        '|',
        Event.isTacticalShiftEvent,
    ]

    fromEventMatcher = [
        Event.isPassEvent,
        '|',
        Event.isShotEvent,
        '|',
        Event.isClearanceEvent,
        '|',
        Event.isGoalKeeperEvent,
    ]

    @classmethod
    def onNew(cls, self):
        self._fromEvent = None
        self._toEvent = None

    @property
    def fromToPair(self):
        fromEvent = None
        toEvent = None
        error = None

        try:
            eventee = As(Event)(self.row)
            candidates = R.pipe(
                R.filter(lambda event: As(Event)(event)
                         ['index'] <= eventee['index']),
                R.sort_by(lambda event: -As(Event)(event)['index']),
            )(eventee.withinPossessionEvents)

            toEvent = candidates.pop(0)
            while len(candidates) > 0:
                candidate = candidates.pop(0)
                if Matcher.isMatch(As(Event)(candidate), self.toEventIgnoreMatcher):
                    continue
                if Matcher.isMatch(As(Event)(candidate), self.toEventMatcher):
                    toEvent = candidate
                    continue

                candidates.insert(0, candidate)
                break

            while len(candidates) > 0:
                candidate = candidates.pop(0)
                if Matcher.isMatch(As(Event)(candidate), self.fromEventIgnoreMatcher):
                    continue
                if Matcher.isMatch(As(Event)(candidate), self.fromEventMatcher):
                    fromEvent = candidate
                break

        except Exception as e:
            error = str(e)
            print(e)

        return [fromEvent, toEvent, error]
