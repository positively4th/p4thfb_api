

class Name:

    prototypes = []

    @staticmethod
    def name(cls):
        return 'Player Name'

    def _value(self):
        return self.eventee['playerName']

    @property
    def value(self):
        raise Exception('Not implemented')
