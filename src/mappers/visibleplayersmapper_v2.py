
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.nestedquery import NestedQuery

from src.mappers.mapper_v2 import Mapper
from src.mappers.storemapper_v2 import StoreMapper


class VisiblePlayersMapper(Leaf):

    prototypes = [StoreMapper] + StoreMapper.prototypes + \
        [Mapper] + Mapper.prototypes

    columnSpecs = {
    }

    def getDataQuery(self, __ids) -> tuple:
        if self._dataQuery is None:

            columns = '''
                _f.__id,
                _e.__id as event__id, _e.id as "eventId",
                _ts.__id as threesixty__id, 
                _ff.teammate = 'True' as teammate, 
                _ff.actor = 'True' as actor, 
                _ff.keeper = 'True' as keeper, 
                cast(_lx.__value as real) x,
                cast(_ly.__value as real) y
            '''.format()

            maybeColumns = []

            tables = '''
                :<-filter>: _f 
                inner join threesixty _ts on _ts.__id = _f.__id 
                inner join "threesixty<-freeze_frame" _ffts on _ffts.threesixty__id = _ts.__id
                inner join freeze_frame _ff on _ff.__id = _ffts.freeze_frame__id 
                inner join "freeze_frame<-location" _fflx on _fflx.freeze_frame__id = _ff.__id and _fflx.__index % 2 = 0
                inner join "location" _lx on _lx.__id = _fflx.location__id
                inner join "freeze_frame<-location" _ffly on _ffly.freeze_frame__id = _ff.__id and _ffly.__index = _fflx.__index + 1
                inner join "location" _ly on _ly.__id = _ffly.location__id  
                inner join events _e on _e.id = _ts.event_uuid
            '''

            self._dataQuery = self._buildSelect(
                tables, columns, maybeColumns)

        filter = self['db'].constantRows({
            '__id': 'text',
        }, [{'__id': __id} for __id in __ids])
        qs = {'filter': filter}

        q = NestedQuery.buildCTE(self._dataQuery, qs)
        return (q, {})

    @classmethod
    def onNew(cls, self):
        self._dataQuery = None

    async def event__id2__id(self, event__id: str) -> list:
        pipes = self['db'].createPipes()

        filter, p, _ = pipes.member(
            'select _e.__id from events _e', '__id', event__id)
        qs = {
            'filter': filter
        }

        q = NestedQuery.buildCTE('''
        select _ts.__id
        from :<-filter>: _f
        inner join events _e on _e.__id = _f.__id
        inner join threesixty _ts on _ts.event_uuid = _e.id 
        ''', qs)

        rows = await self['db'].query((q, p))
        return [r['__id'] for r in rows]
