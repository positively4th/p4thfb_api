from contrib.pyas.src.pyas_v3 import Leaf

from src.tools.matcher import Matcher
from src.mappers.event.constants import Constants
from src.mixins.event.event import Event as Event0


class Event(Leaf):

    prototypes = [
        Event0, *Event0.prototypes,
    ]

    approvedVersions = {
        'application': '==0.0.0',
    }

    def matchRelatedEvents(self, filter):
        relatedEvents = self['relatedEvents']
        related = relatedEvents['related'] if 'related' in relatedEvents else [
        ]
        return Matcher.match(related, filter)

    def relatedGoalKeeperEvents(self):

        def filter(event):
            return event['typeId'] == Constants.goalKeeperTypeId

        return self.matchRelatedEvents(filter)

    @property
    def xG(self):
        if not 'type' in self:
            return None
        _type = self['type']
        if not 'xG' in _type:
            return None
        return _type['xG']

    @property
    def outcomeId(self):
        if not 'type' in self:
            return None
        _type = self['type']
        if not 'outcomeId' in _type:
            return None
        return _type['outcomeId']

    @property
    def assistingEvent(self):
        tagRelatedEventsMap = self['relatedEvents']
        assistEvent = tagRelatedEventsMap[Constants.assistingPassTag] \
            if Constants.assistingPassTag in tagRelatedEventsMap else []
        assert len(assistEvent) <= 1
        return assistEvent[0] if len(assistEvent) > 0 else None

    @property
    def possessionFirstEvent(self):
        tagRelatedEventsMap = self['relatedEvents']
        event = tagRelatedEventsMap[Constants.possessionFirstTag] \
            if Constants.possessionFirstTag in tagRelatedEventsMap else []
        assert len(event) <= 1
        return event[0] if len(event) > 0 else None

    @property
    def withinPossessionEvents(self):
        tagRelatedEventsMap = self['relatedEvents']
        possessionEvents = tagRelatedEventsMap[Constants.withinPossessionTag] \
            if Constants.withinPossessionTag in tagRelatedEventsMap else []
        assert len(possessionEvents) >= 1
        return possessionEvents
