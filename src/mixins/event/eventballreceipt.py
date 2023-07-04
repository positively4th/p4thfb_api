from contrib.pyas.src.pyas_v3 import Leaf


class EventBallReceipt(Leaf):

    prototypes = []

    incompleteOutcomeId = '9'

    def isSuccessOutcome(self):
        assert 'outcomeId' in self
        return self['outcomeId'] != self.incompleteOutcomeId
