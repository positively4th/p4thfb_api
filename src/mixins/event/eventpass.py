from contrib.pyas.src.pyas_v3 import Leaf


class EventPass(Leaf):

    prototypes = []

    groundHeightId = '1'
    lowHeightId = '2'
    highHeightId = '3'

    cornerTypeId = '61'
    freeKickTypeId = '62'
    goalKickTypeId = '63'
    interceptionTypeId = '64'
    kickOfTypeId = '65'
    recoveryTypeId = '66'
    throwInTypeId = '67'

    idTypeMap = {
        '62': 'Free Kick',
        '87': 'Open Play',
        '88': 'Penalty',
    }

    typeIdMap = {v: k for k, v in idTypeMap.items()}

    incompleteOutcomeId = '9'
    injuryClearanceOutcomeId = '74'
    outOutcomeId = '75'
    passOffsideOutcomeId = '76'
    unknownOutcomeId = '77'

    def isSuccess(self):
        assert 'outcomeId' in self
        if self['outcomeId'] == self.unknownOutcomeId:
            return None
        return self['outcomeId'] not in (self.incompleteOutcomeId,
                                         self.injuryClearanceOutcomeId,
                                         self.outOutcomeId,
                                         self.passOffsideOutcomeId)
