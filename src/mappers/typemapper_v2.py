
from contrib.p4thpydb.db.nestedquery import NestedQuery
from src.mappers.mapper_v2 import Mapper
from src.mappers.storemapper_v2 import StoreMapper


class TypeMapper():

    prototypes = [StoreMapper] + StoreMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    columnSpecs = {}

    indexes = []

    queries = {
    }

    querySpecs = {}  # like in PassMapper_v2
    eventType = None  # like 'shot'

    @classmethod
    def onNew(cls, self):

        for name, spec in self.querySpecs.items():
            self.__class__.queries[name] = self._buildSelect(
                spec['tables'], spec['columns'], spec['maybeColumns'])

    def getDataQuery(self, __ids) -> tuple:
        qs = {**self.queries}
        filter = self['db'].constantRows({
            '__id': 'text',
        }, [{'__id': __id} for __id in __ids])
        qs['filter'] = filter

        q = NestedQuery.buildCTE(
            self.queries[self.eventType], qs)
        return (q, {})

    async def event__id2__id(self, event__id: str) -> list:
        qs = {**self.queries}
        ids = event__id if isinstance(
            event__id, list) else [event__id]
        ids = [{'event__id': id} for id in ids]
        qs['filter'] = self['db'].constantRows({
            'event__id': 'text',
        }, ids)

        q = NestedQuery.buildCTE('''
        select _s.__id
        from :<-filter>: _f
        inner join "events<-{eventType}" _ep on _ep.events__id = _f.event__id
        inner join {eventType} _s on _s.__id = _ep.{eventType}__id 
        '''.format(eventType=self.eventType), qs)

        rows = await self['db'].query((q, {}))
        return [r['__id'] for r in rows]
