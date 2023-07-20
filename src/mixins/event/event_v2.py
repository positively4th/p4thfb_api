import asyncio
from collections.abc import Iterable
import ramda as R
from inspect import iscoroutine

from contrib.pyas.src.pyas_v3 import T
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf

from src.tools.matcher import Matcher
from src.mappers.event.constants import Constants
from src.store.autostores import getAutoStores
from src.mixins.event.event import Event as Event0


async def _type(val, key, self):
    typeIdTableMap = {
        Constants.carryTypeId: 'carry',
        Constants.clearanceTypeId: 'clearance',
        Constants.duelTypeId: 'duel',
        Constants.goalKeeperTypeId: 'goalkeeper',
        Constants.interceptionTypeId: 'interception',
        Constants.passTypeId: 'pass',
        Constants.shotTypeId: 'shot',
        Constants.tacticalShiftTypeId: 'tactics',
    }

    typeIdStorePrefixMap = {
        Constants.goalKeeperTypeId: 'goalKeeper',
    }

    typeId = self['typeId']
    if not typeId in typeIdTableMap:
        return None
    table = typeIdTableMap[typeId]

    storee = typeIdStorePrefixMap[typeId] if typeId in typeIdStorePrefixMap else table
    storee = self['stores'][storee + 'Store']

    return await storee.byEvent(self['__id'])


async def _visibleArea(val, key, self):
    visibleAreaStore = self['stores']['visibleAreaStore']
    return await visibleAreaStore.byEvent((self['__id']))


async def _visiblePlayers(val, key, self):
    visiblePlayersStore = self['stores']['visiblePlayersStore']
    return await visiblePlayersStore.byEvent(self['__id'])


async def _relatedEvents(val, key, self):
    return await self['stores']['relatedEventsStore'].byEvent((self['__id']))


async def _possesionEvents(val, key, self):
    possessionEventsStore = self['stores']['possessionEventsStore']
    return await possessionEventsStore.byEvent(self['__id'])


class Event(Leaf):

    prototypes = [
        Event0, *Event0.prototypes,
    ]

    columnSpecs = {
        'stores': {
            'transformer': T.virtual(lambda val, key, classee: getAutoStores() if classee.autoStores is None else classee.autoStores),
        },
        'possessionEvents': {
            'transformer': T.async_fallback(_possesionEvents),
        },
        'visibleArea': {
            'transformer': T.async_fallback(_visibleArea),
        },
        'visiblePlayers': {
            'transformer': T.async_fallback(_visiblePlayers),
        },
        'type': {
            'transformer': T.async_fallback(_type),
        },
        'relatedEvents': {
            'transformer': T.async_fallback(_relatedEvents),
        },
    }

    approvedVersions = {
        'application': '==1.0.0',
    }

    autoStores = None

    @classmethod
    def isEvent(cls, e: dict) -> bool:
        return e is not None and isinstance(e, dict) and 'event__id' in e and 'typeId' in e and 'playerId' in e

    @classmethod
    async def export(cls, events: Iterable[dict], features: dict = {}) -> dict | list:

        def ensureCoro(val):
            if iscoroutine(val):
                return val

            f = asyncio.Future()
            f.set_result(val)
            return f

        height = len(events)
        width = len(features)
        coros = [None] * width * height

        for y, event in enumerate(events):
            for x, feature in enumerate(features.keys()):
                coros[y*width+x] = ensureCoro(As(Event)(event)[feature])

        cores = await asyncio.gather(*coros, return_exceptions=True)

        res = [{**event} for event in events]
        for x, feature in enumerate(features.keys()):
            for y, event in enumerate(events):
                res[y][feature] = cores[y*width+x]

        for f, fs in features.items():
            if fs is None:
                continue

            children = R.unnest([e[f] for e in res if e[f] is not None])
            children = await cls.export(children, fs)
            for e in res:
                if e[f] is None:
                    continue
                e[f] = [children.pop(0) for _ in e[f]]

        return res

    async def matchRelatedEvents(self, filter):
        relatedEvents = await self['relatedEvents']

        related = R.filter(
            lambda re: Constants.relatedTag in re['tag'])(relatedEvents)
        # relatedEvents['related'] if 'related' in relatedEvents else []
        return Matcher.match(related, filter)

    async def relatedGoalKeeperEvents(self):

        def filter(event):
            return event['typeId'] == Constants.goalKeeperTypeId

        return await self.matchRelatedEvents(filter)

    @property
    async def xG(self):
        _type = await self['type']
        if _type is None or not 'xG' in _type:
            return None
        return _type['xG']

    @property
    async def outcomeId(self):
        if not 'type' in self:
            return None
        _type = await self['type']
        if not 'outcomeId' in _type:
            return None
        return _type['outcomeId']

    @property
    async def assistingEvent(self):
        relatedEvents = await self['relatedEvents']
        assistEvent = R.filter(
            lambda re: Constants.assistingPassTag in re['tag'])(relatedEvents)
        assert len(assistEvent) <= 1
        return assistEvent[0] if len(assistEvent) > 0 else None

    @property
    async def possessionFirstEvent(self):
        relatedEvents = await self['relatedEvents']
        event = R.filter(
            lambda re: Constants.possessionFirstTag in re['tag'])(relatedEvents)
        assert len(event) <= 1
        return event[0] if len(event) > 0 else None

    @property
    async def withinPossessionEvents(self):
        relatedEvents = await self['relatedEvents']
        possessionEvents = R.filter(
            lambda re: Constants.withinPossessionTag in re['tag'])(relatedEvents)

        assert len(possessionEvents) >= 1
        return possessionEvents
