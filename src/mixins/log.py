import logging
from random import random

from contrib.pyas.src.pyas_v3 import Leaf


class Log(Leaf):

    prototypes = []

    logging = logging

    def log(self, level, msg, *args, p=None, **kwargs):

        if not hasattr(self.logging, level):
            self.logging.error('Invalid log level {}:'.format(level))
            self.logging.error(*args, **kwargs)
            return

        if p is not None and random() > p:
            return

        l = getattr(self.logging, level)
        l(self.logPrefix()+msg, *args, **kwargs)

    def logPrefix(self) -> str:
        return ''
