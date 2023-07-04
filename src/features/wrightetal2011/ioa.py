from os.path import dirname
from os.path import sep as pathsep
from contrib.pyas.src.pyas_v3 import Leaf
from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011
from src.features.feature import Feature
from mixins.event.event import Event
from mixins.event.eventshot import EventShot
from mixins.event.eventduel import EventDuel
from mixins.event.eventinterception import EventInterception
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

    prototypes = [Wrightetal2011] + Wrightetal2011.prototypes

    @property
    def value(self):

        def getName():

            name = Feature.featureName(self.__class__)
            self.addMetaKeyVal('Play Pattern', '{} ({})'
                               .format(self.event['playPatternName'], self.event['playPatternId']))
            firstEvent = None \
                if MapperEventConstants.possessionFirstTag not in self.event['relatedEvents'] \
                else self.event['relatedEvents'][MapperEventConstants.possessionFirstTag]
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

        return 1 if getName() == Feature.featureName(self.__class__) else 0


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
