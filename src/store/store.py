import ramda as R
import asyncio
import threading
import logging
from inspect import iscoroutine

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T
from contrib.pyas.src.pyas_v3 import As

from src.store.queue.queueitem import QueueItem
from src.mixins.log import Log


class Store(Leaf):

    prototypes = [Log] + Log.prototypes

    batchSize = 1000
    batchDelay = 0.0001
    Mapper = None

    columnSpecs = {
        'db': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },
        'loadedMap': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else {}),
        },
        'pendingMap': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else {}),
        },
        'mapperee': {
            'transformer': T.virtual(lambda val, key, classee: As(classee.Mapper)({'db': classee['db'], 'pipes': classee['db'].createPipes()})),
        },
        'batchSize': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else classee.batchSize),
        },
        'batchDelay': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else classee.batchDelay),
        },

    }

    @classmethod
    async def logRunTime(cls, f: callable, logger: callable, meta: dict = {}):
        res = f()
        if iscoroutine(res):
            res = await res
        return res

    def logDuration(self, data: dict):
        self.log('debug', '{storeId} fetched {count} items in {elapsedTime} (system: {systemTime}, user: {userTime})'
                 .format(storeId=self.__class__.__name__, count=data['count'], elapsedTime=data['elapsed'], systemTime=data['system'],
                         userTime=data['user']))

    @classmethod
    def debug(cls):
        logging.basicConfig(
            level=logging.DEBUG,  # <-- update to DEBUG
            format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )

    @classmethod
    async def monitor(cls):
        while True:
            tasks = [
                t for t in asyncio.all_tasks()
                if t is not asyncio.current_task()
            ]

            for t in tasks:
                print('\n\n', t.get_name())
                print(t)
                t.print_stack(limit=5)
            await asyncio.sleep(1)

    @classmethod
    def onNew(cls, self):
        self.queueTask = None
        self.producer = asyncio.Queue()
        self.pendingMapLock = threading.Lock()

    async def process(self, queueItems):
        db = self['db']
        mapperee = self['mapperee']
        __ids = [As(QueueItem)(queueItem)['__id']
                 for queueItem in queueItems]
        qpT = mapperee.dataQuery(__ids)

        rows = await db.query(qpT)
        rows = R.group_by(lambda storeItem: storeItem['__id'])(rows)

        for queueItem in queueItems:
            __id = queueItem['__id']
            queueItemee = As(QueueItem)(queueItem)
            self.log('info', 'item {} ready to be delivered'.format(__id))
            queueItemee['result'] = rows[__id] if __id in rows else []
        return queueItems

    @property
    def mapperName(self):
        res = As(self.Mapper).__name__
        res = res.split('_')
        return res[0]

    def logPrefix(self):
        return '[{} Store] '.format(self.mapperName)

    def start(self):

        def deliverItems(queueItems):
            with self.pendingMapLock:
                for queueItem in queueItems:
                    queueItemee = As(QueueItem)(queueItem)
                    __id = queueItemee['__id']
                    self['loadedMap'][__id] = queueItem['result']
                    self.log('info',
                             'item {} added to loaded map'.format(__id))
                    if not __id in self['pendingMap']:
                        continue
                    qs = self['pendingMap'].pop(__id)
                    for q in qs:
                        q.put_nowait(queueItem)
                        self.log('info', 'item {} delivered'.format(__id))

        async def helper(name):

            def logWaitWrapper(data: dict, result):
                return {**data, 'count': len(result)}

            async def waitForSeveral():
                items = []
                items.append(await self.producer.get())
                while len(items) < self['batchSize']:
                    await asyncio.sleep(self['batchDelay'])
                    try:
                        items.append(self.producer.get_nowait())
                    except asyncio.QueueEmpty:
                        break
                return items

            while True:
                items = await self.logRunTime(waitForSeveral, {'tag': 'waitForSeveral'}, logWaitWrapper)

                self.log('info', '{} is processing'.format(name))
                try:
                    queueItems = await self.logRunTime(lambda: self.process(items),
                                                       {
                                                           'tag': 'process',
                                                           'count': len(items)
                    })
                except Exception as e:
                    queueItems = [{**item, **{'result': e}} for item in items]
                deliverItems(queueItems)

        assert self.queueTask is None

        # loop = asyncio.get_running_loop()
        # self.queueTask = loop.create_task(helper())
        # loop.run_until_complete(self.queueTask)
        name = self.__class__.__name__
        self.queueTask = asyncio.create_task(
            helper(name), name=name)
        self.log('info', 'Started store', name)
        # return self.queueTask

    def ensureOpen(self):
        if self.queueTask is not None:
            return
        self.start()

    async def waitFor(self, __id: str) -> list[dict]:

        with self.pendingMapLock:
            qs = self['pendingMap'][__id] if __id in self['pendingMap'] else []
            q = asyncio.Queue()
            qs.append(q)
            self['pendingMap'][__id] = qs

        self.log('info', 'adding {} to queue.'.format(__id))
        if len(qs) == 1:
            await self.producer.put({
                '__id': __id,
            })
        return await q.get()

    async def get(self, id: str | list[str] | tuple[str]) -> list[dict]:

        if isinstance(id, str):
            items = await self.get([id])
            return items[id] if id in items else None

        self.ensureOpen()

        pendingIds = []

        res = {}
        for __id in id:
            if __id in self['loadedMap']:
                res[__id] = self['loadedMap'][__id]
            else:
                pendingIds.append(__id)

        tasks = asyncio.gather(*(self.waitFor(__id)
                               for __id in pendingIds), return_exceptions=True)
        try:
            queueItems = await tasks
        except Exception as e:
            self.log('error', e)
            raise e

        es = []

        for qi in queueItems:
            r = qi['result']
            if isinstance(r, Exception):
                es.append(r)
            else:
                res[qi['__id']] = r
        for e in es:
            raise e

        return res
