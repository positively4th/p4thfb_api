import ramda as R
from os.path import dirname
from os.path import sep as pathsep

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As

from src.tools.matcher import Matcher
from src.mixins.event.event import Event as Event_v1
from src.mixins.event.event_v2 import Event


class Feed(Leaf):

    prototypes = []

    columnSpecs = {
        'index': {
            'transformer': lambda val, key, feedee: val if key in feedee else None,
        },
        'relatedEvents': {
            'transformer': lambda val, key, feedee: val if key in feedee else None,
        },
    }

    toEventMatcher = [
        Event_v1.isPossessionTeamEvent,
        '&',
        [
            Event_v1.isDribbleEvent,
            '|',
            Event_v1.isCarryEvent,
        ]
    ]

    toEventIgnoreMatcher = [
        ['!', Event_v1.isPossessionTeamEvent],
        '|',
        Event_v1.isDribbledPastEvent,
    ]

    fromEventIgnoreMatcher = [
        ['!', Event_v1.isPossessionTeamEvent],
        '|',
        Event_v1.isBallReceiptEvent,
        '|',
        Event_v1.isBadBehaviourEvent,
        '|',
        Event_v1.isTacticalShiftEvent,
    ]

    fromEventMatcher = [
        Event_v1.isPassEvent,
        '|',
        Event_v1.isShotEvent,
        '|',
        Event_v1.isClearanceEvent,
        '|',
        Event_v1.isGoalKeeperEvent,
    ]

    @classmethod
    def onNew(cls, self):
        self._fromEvent = None
        self._toEvent = None

    @property
    async def fromToPair(self):
        fromEvent = None
        toEvent = None
        error = None

        try:
            eventee = As(Event)(self.row)
            candidates = R.pipe(
                R.filter(lambda event: As(Event)(event)
                         ['index'] <= eventee['index']),
                R.sort_by(lambda event: -As(Event)(event)['index']),
            )(await eventee.withinPossessionEvents)

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
