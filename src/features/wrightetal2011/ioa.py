
from contrib.pyas.src.pyas_v3 import As

from features.wrightetal2011.wrightetal2011 import Wrightetal2011
from src.features.feature import Feature
from src.mixins.classnamed import ClassNamed
from mixins.event.event import Event
from src.mixins.event.eventshot import EventShot
from src.mixins.event.eventduel import EventDuel
from src.mixins.event.eventinterception import EventInterception
from src.mappers.event.constants import Constants as MapperEventConstants

nameIOAFreeKick = 'IOAFreeKick'
nameIOACorner = 'IOACorner'
nameIOAThrowIn = 'IOAThrowIn'
nameIOAInterception = 'IOAInterception'
nameIOASuccessfulTackle = 'IOASuccessfulTackle'
nameIOAOther = 'IOAOther'
nameIOAGoalKick = 'IOAGoalKick'
nameIOAKickOff = 'IOAKickOff'
nameIOAPenalty = 'IOAPenalty'


class IOA:

    playPatternIdNameMap = {
        Event.playPatternIdMap['fromFreeKick']: nameIOAFreeKick,
        Event.playPatternIdMap['fromCorner']: nameIOACorner,
        Event.playPatternIdMap['fromThrowIn']: nameIOAThrowIn,
        Event.playPatternIdMap['fromGoalKick']: nameIOAGoalKick,
        Event.playPatternIdMap['fromKickOff']: nameIOAKickOff,
    }

    prototypes = [
        Wrightetal2011, *Wrightetal2011.prototypes
    ]

    def _value(self, relatedEvents):
        def getName():

            name = As(Feature).featureName(self.__class__)
            self.addMetaKeyVal('Play Pattern', '{} ({})'
                               .format(self.event['playPatternName'], self.event['playPatternId']))
            firstEvent = None \
                if MapperEventConstants.possessionFirstTag not in self.event['relatedEvents'] \
                else relatedEvents[MapperEventConstants.possessionFirstTag]
            if firstEvent:
                firstEvent = firstEvent[0]
                self.addMetaKeyVal('First Event Type', '{} ({})'
                                   .format(firstEvent['typeName'], firstEvent['typeId']))

            if name == nameIOAPenalty and self.event['typeId'] == MapperEventConstants.shotTypeId \
                    and self.event['type']['typeId'] == EventShot.penaltyTypeId:
                return nameIOAPenalty

            if name == nameIOASuccessfulTackle and firstEvent['typeId'] == MapperEventConstants.duelTypeId \
                    and firstEvent['type']['outcomeId'] == EventDuel.wonOutcomId:
                return nameIOASuccessfulTackle

            if name == nameIOAInterception and firstEvent['typeId'] == MapperEventConstants.interceptionTypeId \
                    and firstEvent['type']['outcomeId'] in (
                    EventInterception.wonOutcomeId,
                    EventInterception.successOutcomeId,
                    EventInterception.successInPlayOutcomeId):
                return nameIOAInterception

            if self.event['playPatternId'] in self.playPatternIdNameMap.keys():
                return self.playPatternIdNameMap[self.event['playPatternId']]

            return nameIOAOther

        return 1 if getName() == ClassNamed.name(self) else 0

    @property
    def value(self):
        raise Exception('Not implemented')
