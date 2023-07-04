from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.mapper_v2 import Mapper
from src.mappers.storemapper_v2 import StoreMapper


class VisibleAreaMapper(Leaf):

    prototypes = [StoreMapper] + StoreMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    columnSpecs = {}

    columns = '''
        _f.__id, 
        _e.__id as event__id, _e.id as "eventId",
        cast(_vax.__value as real) as x,
        cast(_vay.__value as real) as y,
        _tvax.__index / 2 as "index"
    '''.format()

    maybeColumns = []

    tables = '''
        :<-filter>: _f
        inner join threesixty _ts on _ts.__id = _f.__id 
        left join "threesixty<-visible_area" _tvax on _tvax.threesixty__id = _ts.__id and _tvax.__index % 2 = 0
        left join "visible_area" _vax on _vax.__id = _tvax.visible_area__id
        left join "threesixty<-visible_area" _tvay on (
          _tvay.threesixty__id = _ts.__id and _tvay.__index = _tvax.__index + 1)
        left join "visible_area" _vay on _vay.__id = _tvay.visible_area__id
        inner join events _e on _e.id = _ts.event_uuid
    '''

    queries = {}

    @classmethod
    def onNew(cls, self):

        if not 'visibleArea' in cls.queries:
            cls.queries['visibleArea'] = self._buildSelect(
                cls.tables, cls.columns, cls.maybeColumns)

    def getDataQuery(self, __ids) -> tuple:
        qs = self.queries
        filter = self['db'].constantRows({
            '__id': 'text',
        }, [{'__id': __id} for __id in __ids])
        qs['filter'] = filter

        q = NestedQuery.buildCTE(self.queries['visibleArea'], qs)
        return (q, {})

    async def event__id2__id(self, event__id: str) -> list:
        pipes = self['db'].createPipes()

        filter = self['db'].constantRows({
            'event__id': 'text',
        }, [{'event__id': __id} for __id in [event__id]])
        qs = {
            'filter': filter
        }

        q = NestedQuery.buildCTE('''
        select distinct _ts.__id
        from :<-filter>: _f
        inner join events _e on _e.__id = _f.event__id
        inner join threesixty _ts on _ts.event_uuid = _e.id 
        ''', qs)

        rows = await self['db'].query((q, {}))
        res = [r['__id'] for r in rows]
        return res
