
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.mapper_v2 import Mapper
from src.mappers.indexmapper import IndexMapper
from src.mappers.storemapper_v2 import StoreMapper
from src.mappers.index import Index
from src.mappers.event.eventmapper_v2 import EventMapper


class PossessionEventsMapper(Leaf):

    prototypes = [StoreMapper] + StoreMapper.prototypes + \
        [IndexMapper] + IndexMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    columnSpecs = {}

    indexes = [
        {
            'table': 'events',
            'parts': [
                ['file', Index.quote]
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['index', Index.quote, Index.cast, 'int']
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['possession', Index.quote]
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['possession', Index.quote, Index.cast, 'int']
            ]
        },
        {
            # remove ?
            'table': 'events',
            'parts': [
                ['file', Index.quote],
                ['possession', Index.quote, Index.cast, 'int']
            ]
        },
        {
            'table': 'events',
            'parts': [
                ['file', Index.quote],
                ['possession', Index.quote],
                ['index', Index.quote, Index.cast, 'int']
            ]
        },

    ]

    queries = {

        'possessionEvents':
        '''
        select _f.__id, _e.__id event__id
        from :<-filter>: as _f
        left join events as _e on row(_e.file::text, _e.possession::text)::text = _f.__id
        '''.format(),

    }

    @classmethod
    def onNew(cls, self):
        pass

    @classmethod
    async def possession__id(cls, db, row):
        q = 'select row(file::text, possession::text)::text __id from ({}) _q'.format(db.constantRows({
            'file': 'text',
            'possession': 'text',
        }, [row]))
        ids = await db.query((q, {}))
        return ids[0]['__id'] if len(ids) == 1 else None

    def getDataQuery(self, x__ids) -> tuple:
        qs = {
            **EventMapper.queries,
            **self.queries
        }
        filter = self['db'].constantRows({
            '__id': 'text',
        }, [{'__id': __id} for __id in x__ids])
        # rows = self['db'].query((filter, {}), fetchAll=True)
        qs['filter'] = filter

        q = NestedQuery.buildCTE(
            self.queries['possessionEvents'], qs)
        # rows = self['db'].query((q, {}), fetchAll=True)
        return (q, {})

    async def event__id2__id(self, event__id: str) -> list:
        pipes = self['db'].createPipes()
        qpT = (
            'select row(_e.file::text, _e.possession::text)::text __id, _e.__id event__id from events _e', {})
        qpT = pipes.member(qpT, 'event__id', [event__id])
        rows = await self['db'].query(qpT)
        return [r['__id'] for r in rows]
