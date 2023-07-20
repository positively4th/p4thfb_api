from src.mappers.event.constants import Constants

goalOutcomeId = Constants.Type.Shot.goalOutcomeId


class OutcomeGoal:

    prototypes = []

    def _value(self, outcomeId):
        return int(outcomeId == goalOutcomeId)

    @property
    async def value(self):
        raise Exception('Not implemented')
