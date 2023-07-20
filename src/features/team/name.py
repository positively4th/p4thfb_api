
class Name:

    prototypes = []

    @staticmethod
    def name(cls):
        return 'Team Name'

    def _value(self):
        return self.eventee['eventTeamName']

    @property
    def value(self):
        raise Exception('Not implemented.')
