import json
from copy import copy
from xxhash import xxh32

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf


class Index(Leaf):

    columnSpecs = {
        'table': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },

        'parts': {
            'transformer': lambda val, key, classee: val if key in classee.row else None,
        },
    }

    @staticmethod
    def identity(expr, pipe, quote=None):
        return r'{expr}'.format(expr=expr), pipe

    @staticmethod
    def quote(expr, pipe, quote=lambda v: v):
        return r'{expr}'.format(expr=quote(expr)), pipe

    @staticmethod
    def cast(expr, pipe, quote=None):
        type = pipe.pop(0)
        return r'cast({expr} as {type})'.format(expr=expr, type=type), pipe

    @staticmethod
    def runPipe(quote, pipe):
        _pipe = copy(pipe) if isinstance(pipe, (tuple, list)) else (pipe, )
        val = ''
        while len(_pipe) > 0:
            op = _pipe.pop(0)
            if isinstance(op, str):
                val += op
            elif isinstance(op, (list, tuple)):
                val += Index.runPipe(quote, op)
            else:
                val, _pipe = op(val, _pipe, quote=quote)
        return val

    @property
    def name(self):
        q = self.createQuery(quote=lambda v: v, name='')
        _hash = str(xxh32(q).hexdigest())
        return 'indexed_' + q + '_' + _hash

    def createQuery(self, quote=lambda v: v, name=None):
        parts = [
            self.runPipe(quote, p) for p in self['parts']
        ]
        table = quote(self['table'])
        _name = quote(self.name if name is None else name)
        q = r'create index if not exists {name} on {table} ({parts})'\
            .format(name=_name, table=table, parts=', '.join(parts))
        return q
