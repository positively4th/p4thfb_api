from src.mixins.versionguard import globalVersionGuard
from src.mappers.event.constants import Constants
from src.mixins.classidentified import ClassIdentified
from src.mixins.classnamed import ClassNamed


class EventException(Exception):
    pass


class Event:

    prototypes = [ClassIdentified, ClassNamed] \
        + ClassIdentified.prototypes + ClassNamed.prototypes \
        + [globalVersionGuard()] + globalVersionGuard().prototypes

    idTypeMap = {
        Constants.dispossessedTypeId: 'Dispossessed',
        Constants.duelTypeId: 'Duel',
        Constants.clearanceTypeId: 'Clearance',
        Constants.interceptionTypeId: 'Interception',
        Constants.shotTypeId: 'Shot',
        Constants.goalKeeperTypeId: 'Goal Keeper',
        Constants.passTypeId: 'Pass',
        Constants.halfEndTypeId: 'Half End',
        Constants.tacticalShiftTypeId: 'Tactical Shift',
        Constants.dribbledPastTypeId:  'Dribbled Past',
        Constants.injuryStoppageTypeId: 'Injury Stoppage',
        Constants.refereeBallDropTypeId: 'Referee Ball-Drop',
        Constants.ballReceiptTypeId: 'Ball Receipt*',
        Constants.carryTypeId: 'Carry',
    }

    columnSpecs = {
        'index': {
            'transformer': lambda val, *_, **__: int(val),
        },
    }

    allowUnapprovedVersion = False

    typeIdMap = {v: k for k, v in idTypeMap.items()}

    playPatternIdMap = {
        'regularPlay': '1',
        'fromCorner': '2',
        'fromFreeKick': '3',
        'fromThrowIn': '4',
        'other': '5',
        'fromCounter': '6',
        'fromGoalKick': '7',
        'fromKeeper': '8',
        'fromKickOff': '9',
    }

    def id(self):
        return self.idTypeMap[self['typeId']]

    def name(self):
        return self.idTypeMap[self['typeId']]

    def isPossessionTeamEvent(self):
        return self['possessionTeamId'] == self['eventTeamId']

    def isDispossessedEvent(self):
        return self['typeId'] == Constants.dispossessedTypeId

    def isPassEvent(self):
        return self['typeId'] == Constants.passTypeId

    def isInterceptionEvent(self):
        return self['typeId'] == Constants.interceptionTypeId

    def isDuelEvent(self):
        return self['typeId'] == Constants.duelTypeId

    def isBlockEvent(self):
        return self['typeId'] == Constants.blockTypeId

    def isShotEvent(self):
        return self['typeId'] == Constants.shotTypeId

    def isClearanceEvent(self):
        return self['typeId'] == Constants.clearanceTypeId

    def isBallReceiptEvent(self):
        return self['typeId'] == Constants.ballReceiptTypeId

    def isBadBehaviourEvent(self):
        return self['typeId'] == Constants.badBehaviourTypeId

    def isTacticalShiftEvent(self):
        return self['typeId'] == Constants.tacticalShiftTypeId

    def isCarryEvent(self):
        return self['typeId'] == Constants.carryTypeId

    def isDribbledPastEvent(self):
        return self['typeId'] == Constants.dribbledPastTypeId

    def isDribbleEvent(self):
        return self['typeId'] == Constants.dribbleTypeId

    def isGoalKeeperEvent(self):
        return self['typeId'] == Constants.goalKeeperTypeId

    def isBallRecoveryEvent(self):
        return self['typeId'] == Constants.ballRecoveryTypeId

    def isSuccessOutcome(self):
        return self['typeId'] == Constants.carryTypeId

    def matchRelatedEvents(self, filter):
        raise Exception('Not implemented.')

    def relatedGoalKeeperEvents(self):
        raise Exception('Not implemented.')

    @property
    def asText(self):

        def get(key):
            return self[key] if key in self else ''

        return 'eventId:{} matchId:{} period:{}, minute:{}, index:{} typeName:{}' \
            .format(get('eventId'), get('matchId'), get('period'), get('minute'), get('index'), get('typeName'))

    @property
    def identifiers(self):
        return {
            '__id': self['__id'],
            'eventId': self['eventId'],
            'matchId': self['matchId'],
            'index': self['index'],
        }

    @property
    def xG(self):
        raise Exception('Not imlplemented.')

    @property
    def outcomeId(self):
        raise Exception('Not imlplemented.')

    @property
    def x(self):
        return self['x']

    @property
    def y(self):
        return self['y']

    @property
    def p(self):
        return [self['x'], self['y'], 1]

    @property
    def assistingEvent(self):
        raise Exception('Not imlplemented.')

    @property
    def possessionFirstEvent(self):
        raise Exception('Not imlplemented.')

    @property
    def withinPossessionEvents(self):
        raise Exception('Not imlplemented.')
