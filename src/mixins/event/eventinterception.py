from contrib.pyas.src.pyas_v3 import Leaf


class EventInterception(Leaf):
    prototypes = []

    lostOutcomId = '1'
    wonOutcomId = '4'
    lostOutOutcomId = '14'
    successOutcomeId = '15'
    successInPlayOutcomeId = '16'
    successOutOutcomeId = '17'

    def isSuccessInPlay(self):
        assert 'outcomeId' in self
        return self['outcomeId'] not in (self.wonOutcomId,
                                         self.successOutcomeId,
                                         self.successInPlayOutcomeId)
