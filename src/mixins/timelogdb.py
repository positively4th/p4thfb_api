from os import times
from numbers import Number
from inspect import iscoroutine
from time import sleep
import asyncio
import threading
import datetime

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T
from contrib.p4thpydb.db.ts import Ts as DBTs


class TimeLogDB(Leaf):

    columnSpecs = {
        'timeLogDB': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },

    }

    def getTimeLogTableSpec(self):

        timeLogTableSpec = {
            'name': "timeLog_v1",
            'columnSpecs': {
                'jiff': {
                    'definition': "TEXT NOT NULL",
                    'transform': DBTs.nullableDateTimeAsStr,
                },
                'identifier': {
                    'definition': "TEXT NOT NULL DEFAULT ''",
                    'transform': DBTs.str,
                },
                'tag': {
                    'definition': "TEXT NOT NULL DEFAULT ''",
                    'transform': DBTs.str,
                },
                'group': {
                    'definition': "TEXT NOT NULL DEFAULT ''",
                    'transform': DBTs.str,
                },
                'error': {
                    'definition': "TEXT NOT NULL DEFAULT ''",
                    'transform': DBTs.emptyNullStr,
                },
                'count': {
                    'definition': "REAL NOT NULL DEFAULT ''",
                    'transform': DBTs.float,
                },
                'elapsed': {
                    'definition': "REAL NOT NULL DEFAULT ''",
                    'transform': DBTs.float,
                },
                'user': {
                    'definition': "REAL NOT NULL DEFAULT ''",
                    'transform': DBTs.float,
                },
                'system': {
                    'definition': "REAL NOT NULL DEFAULT ''",
                    'transform': DBTs.float,
                },
            },
            'primaryKeys': ["jiff", 'identifier']
        }

        with self.timeLogTableSpecLock:
            return timeLogTableSpec

    @property
    def pendingRows(self):
        return self.queue.qsize() if self.queue else 0

    @staticmethod
    def _startQueue(queue, db, getTimeLogTableSpec):

        async def run(queue: asyncio.Queue, orm):
            await orm.ensureTable(getTimeLogTableSpec())
            while True:
                try:
                    await asyncio.sleep(1.0 / float(1.0 + queue.qsize()))
                    row = queue.get_nowait()
                    await orm.insert(getTimeLogTableSpec(), [row])
                except asyncio.QueueEmpty as qe:
                    pass

        orm = db.createORM(db)
        thread_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(thread_loop)
        thread_loop.run_until_complete(
            run(queue, orm))

    def __del__(self):
        while self.pendingRows() > 0:
            print('{} is waiting for logging to complete. {} pending.',
                  self.__class__.__name__, self.pendingRows)
            sleep(1.0)

    @classmethod
    def onNew(cls, self):
        timeLogDB = self['timeLogDB']
        self.timeLogIsActive = timeLogDB is not None
        if not self.timeLogIsActive:
            return
        self.timeLogTableSpecLock = threading.Lock()
        db = self['timeLogDB']
        self.queue = asyncio.Queue()
        self.thread = threading.Thread(
            target=cls._startQueue, name=self.__class__.__name__, args=(self.queue, db.clone(), lambda: self.getTimeLogTableSpec()), daemon=True).start()

    async def logRunTime(self, f: callable, staticData: dict = {},
                         dataAdder: callable = lambda meta, result: {**meta, 'result': result}):
        ts0 = times()
        error = None
        try:
            res = f()
            res = (await res) if iscoroutine(res) else res
            assert not iscoroutine(res)
        except Exception as e:
            error = str(e)
            res = None
            raise e
        finally:
            ts1 = times()
            dts = {
                k: getattr(ts1, k) - getattr(ts0, k) for k in dir(ts1)
                if isinstance(getattr(ts1, k), Number)
            }
            _meta = dataAdder({
                'jiff': datetime.datetime.now(),
                'error': error,
                **dts,
                **staticData
            }, res)
            await self._logDuration(_meta)
        return res

    def asRuntimeLogged(self, f: callable, identifier: str = None, tag: str = None, group: str = None, count: float = None):

        async def logger(*args, **kwargs):
            return await self._logDuration(*args, **kwargs)

        async def helper(*args, **kwargs):

            def fwrapper():
                return f(*args, **kwargs)

            return await self.logRunTime(fwrapper, {
                'identifier': identifier,
                'tag': tag,
                'group': group,
                'count': count,
            })

        return helper

    async def _logDuration(self, data: dict):

        if not self.timeLogIsActive:
            return
        try:
            coro = super().logDuration(data)
            if iscoroutine(coro):
                await coro
        except AttributeError:
            pass

        row = {
            'identifier': self.__class__.__name__,
            **data,
        }
        await self.queue.put(row)

    def timeLogReport(self, identifier: str = None, tag: str = None,
                      minJiff: str | datetime.datetime = None, maxJiff: str | datetime.datetime = None,
                      groupBy=None) -> list[dict]:
        if not self.timeLogIsActive:
            return None

        db = self['timeLogDB']
        orm = db.createORM(db)
        pipes = db.createPipes()
        util = db.createUtil()

        qpT = orm.select(self.getTimeLogTableSpec())

        if identifier is not None:
            qpT = pipes.equals(qpT, {'identifier': identifier})

        if tag is not None:
            qpT = pipes.equals(qpT, {'tag': tag})

        if minJiff is not None:
            qpT = pipes.equals(qpT, {'jiff': minJiff}, op='>=')

        if maxJiff is not None:
            qpT = pipes.equals(qpT, {'jiff': maxJiff}, op='<=')

        if groupBy is not None:

            aggregates = {}
            for col in ['count', 'elapsed', 'user', 'system']:
                for agg in ['min', 'avg', 'max']:
                    if agg == 'median':
                        _agg = 'PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cast({} as double precision))'.format(
                            util.quote(col))
                    else:
                        _agg = '{}(cast({} as double precision))'.format(
                            agg, util.quote(col))
                    aggregates['{}_{}'.format(
                        agg, col)] = _agg

            qpT = pipes.aliases(qpT, {
                'identifier': 'identifier',
                'tag': 'tag',
                'elapsed': 'elapsed',
                'user': 'user',
                'system': 'user',
                'count': 'count',
                'elapsedPerUnit': '{} / {}'.format(util.quote('elapsed'), util.quote('count')),
                'systemPerUnit': '{} / {}'.format(util.quote('system'), util.quote('count')),
                'userPerUnit': '{} / {}'.format(util.quote('user'), util.quote('count')),
            })

            qpT = pipes.aggregate(qpT, aggregates, groupBy)

        rows = db.query(qpT)

        return rows
