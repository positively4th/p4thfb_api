import ramda as R
import asyncio
import threading
import logging
import random

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import T
from contrib.pyas.src.pyas_v3 import As

from src.store.queue.queueitem import QueueItem
from src.mixins.log import Log
from src.mixins.contextlogger import ContextLogger
from src.mixins.classnamed import ClassNamed


class Store(Leaf):

    prototypes = [
        Log, *Log.prototypes,
        ClassNamed, *ClassNamed.prototypes,
    ]

    batchSize = 1000
    batchDelay = 0.01
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
    def debug(cls):
        logging.basicConfig(
            level=logging.DEBUG,  # <-- update to DEBUG
            format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )

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

            async def retryGet(delay=0, retries=1):
                try:
                    if self.__class__.__name__.find('EventStore_'):
                        pass

                    return self.producer.get_nowait()
                except asyncio.QueueEmpty as e:
                    if retries > 0:
                        await asyncio.sleep(delay)
                        return await retryGet(retries=retries-1)
                    # self.log('error', 'Empty queue: {}'.format(e))
                return None

            async def waitForSeveral():

                items = []
                if self.__class__.__name__.find('EventStore_'):
                    pass
                while len(items) < self['batchSize']:
                    # try:
                    if self.__class__.__name__.find('EventStore_'):
                        pass
                    item = await retryGet(self['batchDelay'], retries=1)
                    if item is None:
                        if len(items) > 0:
                            break
                    else:
                        items.append(item)

                if self.__class__.__name__.find('EventStore_'):
                    pass
                return items

            while True:
                items = await waitForSeveral()

                self.log('info', '{} is processing'.format(name))
                try:
                    queueItems = await ContextLogger.asLogged(
                        self.process,
                        tag=f"{ self.process.__name__ }:{ ClassNamed.name(self) }",
                        resultHandler=ContextLogger.countResultHandler)(items)
                except Exception as e:
                    queueItems = [{**item, **{'result': e}} for item in items]
                deliverItems(queueItems)

        assert self.queueTask is None

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

    async def get(self, id: str | list[str] | tuple[str], **kwArgs) -> list[dict]:

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

        async def loadNewTG(pendingIds):
            res = {}
            tasks = []
            async with asyncio.TaskGroup() as taskGroup:
                for __id in pendingIds:
                    tasks.append(taskGroup.create_task(self.waitFor(__id)))
            es = []
            for qi in tasks:
                qi = qi.result()
                r = qi['result']
                if isinstance(r, Exception):
                    es.append(r)
                else:
                    res[qi['__id']] = r
            for e in es:
                raise e
            return res

        async def loadNewGather(pendingIds):
            res = {}
            try:
                coros = (self.waitFor(__id) for __id in pendingIds)
                cores = await asyncio.gather(
                    *coros, return_exceptions=True)
            except Exception as e:
                self.log('error', e)
                raise e
            es = []
            for qi in cores:
                r = qi['result']
                if isinstance(r, Exception):
                    es.append(r)
                else:
                    res[qi['__id']] = r
            for e in es:
                raise e
            return res

        async def loadNewAsCompleted(pendingIds):
            res = {}
            tasks = [asyncio.create_task(self.waitFor(
                __id), name=__id) for __id in pendingIds]
            try:
                for task in asyncio.as_completed(tasks):
                    qi = await task
                    r = qi['result']
                    res[qi['__id']] = r
                return res
            except Exception as e:
                print(e)
                raise (e)

        r = random.randint(0, 2)
        if r < 1:
            res.update(await ContextLogger.asLogged(loadNewTG, resultHandler=ContextLogger.countResultHandler)(pendingIds))
        elif r < 2:
            res.update(await ContextLogger.asLogged(loadNewGather, resultHandler=ContextLogger.countResultHandler)(pendingIds))
        else:
            res.update(await ContextLogger.asLogged(loadNewAsCompleted, resultHandler=ContextLogger.countResultHandler)(pendingIds))

        return res
