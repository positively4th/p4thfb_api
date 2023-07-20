from src.features.wrightetal2011.wrightetal2011 import Wrightetal2011


class PDSG:

    prototypes = [
        Wrightetal2011, *Wrightetal2011.prototypes
    ]

    def _value(self, blockerCount):
        self.addMetaKeyVal('blockerCount', str(blockerCount))
        res = (self.minPlayers is None or blockerCount >= self.minPlayers) \
            and (self.maxPlayers is None or blockerCount <= self.maxPlayers)
        return 1 if res is True else 0

    @property
    def value(self):
        raise Exception('Not implemented')
