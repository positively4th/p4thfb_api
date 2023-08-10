import threading
import datetime
from os import times
from numbers import Number
from time import sleep
from queue import Queue
from queue import Empty
from json import loads
from json import dumps

from contrib.pyas.src.pyas_v3 import Leaf
from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import T
from contrib.p4thpydb.db.ts import Ts as DBTs

from src.mixins.log import Log


class TimeLogDB(Leaf):

    prototypes = [
        Log, *Log.prototypes
    ]

    columnSpecs = {
        'timeLogDB': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },
        'isActive': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else None),
        },
        'maxInsertRows': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else classee.maxInsertRows),
        },
        'nextRowWaitTime': {
            'transformer': T.writableEmpty(lambda val, key, classee: val if key in classee.row else classee.nextRowWaitTime),
        },
    }

    maxInsertRows = 250
    nextRowWaitTime = 1.0
    idMetaMap = {}

    @classmethod
    def getTimeLogTableSpec(cls):

        timeLogTableSpec = {
            'name': "timeLog_v2",
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
                'tagPath': {
                    'definition': "TEXT NOT NULL DEFAULT ''",
                    'transform': DBTs.str,
                },
                'traceId': {
                    'definition': "TEXT NOT NULL DEFAULT ''",
                    'transform': DBTs.str,
                },
                'queryString': {
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
                'children_user': {
                    'definition': "REAL NOT NULL DEFAULT ''",
                    'transform': DBTs.float,
                },
                'system': {
                    'definition': "REAL NOT NULL DEFAULT ''",
                    'transform': DBTs.float,
                },
                'children_system': {
                    'definition': "REAL NOT NULL DEFAULT ''",
                    'transform': DBTs.float,
                },
            },
            'primaryKeys': ["jiff", 'identifier']
        }

        with cls.timeLogTableSpecLock:
            return timeLogTableSpec

    @property
    def isPending(self):
        return self.pendingDBOps > 0 or self.pendingRows > 0

    @property
    def pendingRows(self):
        res = 0
        for _, meta in self.idMetaMap.items():
            res += meta['queue'].qsize()
        return res

    @property
    def pendingDBOps(self):
        res = 0
        for _, meta in self.idMetaMap.items():
            res += meta['dbOpQueue'].qsize()
        return res

    @staticmethod
    def _startQueue(queue, dbOpQueue: Queue, threadRow):
        threadTimeLogDB = As(TimeLogDB)(threadRow)
        db = threadTimeLogDB['db']
        timeLogTableSpec = threadTimeLogDB.getTimeLogTableSpec()
        successes = 0
        fails = 0

        orm = db.createORM(db)
        dbOpQueue.put('ensureTable')
        try:
            orm.ensureTable(timeLogTableSpec)
        except Exception as e:
            if not orm.tableExists(timeLogTableSpec):
                raise e
        finally:
            dbOpQueue.get()

        while True:
            rows = [queue.get()]
            dbOpQueue.put('insert')
            try:

                while len(rows) < threadTimeLogDB['maxInsertRows']:
                    try:
                        rows.append(
                            queue.get(True, threadTimeLogDB['nextRowWaitTime']))
                    except Empty:
                        break

                try:
                    orm.insert(timeLogTableSpec, rows)
                    successes += len(rows)
                    threadTimeLogDB.log('info',
                                        f"Pending inserts: { queue.qsize() }. Successes/fails = { successes }/{ fails }", p=0.1
                                        )
                except Exception as e:
                    fails += len(rows)
                    threadTimeLogDB.log(
                        'warning', f"Timelog fail: { str(e) }")
                    for row in rows:
                        queue.put(row)
                    sleep(1.0)
            finally:
                dbOpQueue.get()

    @property
    def isActive(self):
        return self.row and (
            self['timeLogDB'] if self['isActive'] is None else self['isActive']
        )

    def getDBQueue(self, db):
        cls = self.__class__
        dbId = db.id
        if not dbId in cls.idMetaMap:
            cls.idMetaMap[dbId] = dbMeta = {}

            dbMeta['db'] = db
            dbMeta['queue'] = Queue()
            dbMeta['dbOpQueue'] = Queue()

            threadRow = {
                'db': db.clone()
            }

            for key, val in self.row.items():
                if key in ['db']:
                    continue
                try:
                    val = loads(dumps(val))
                    threadRow[key] = val
                except:
                    pass

            thread = threading.Thread(
                target=cls._startQueue,
                name=f"{cls.__name__}: dbId",
                args=(dbMeta['queue'], dbMeta['dbOpQueue'], threadRow), daemon=True)
            thread.start()
            dbMeta['thread'] = thread

        return cls.idMetaMap[dbId]['queue']

    @staticmethod
    def onNewClass(cls):
        cls.timeLogTableSpecLock = threading.Lock()

    def _open(self, staticData: dict = {}, dataAdder: callable = lambda meta, result: {**meta, 'result': result}):

        return {
            'dataAdder': dataAdder,
            **staticData,
            't0': times()
        }

    def _close(self, data, res, error, dataAdder: callable = lambda meta, result: {**meta, 'result': result}):
        if not self.isActive:
            return

        ts1 = times()
        ts0 = data.pop('t0')
        for k in dir(ts1):
            if not isinstance(getattr(ts1, k), Number):
                continue
            data[k] = getattr(ts1, k) - getattr(ts0, k)

        data['jiff'] = datetime.datetime.now()
        data['error'] = error
        data = data.pop('dataAdder')(data, res)
        self._logDuration(data)

    def _logDuration(self, data: dict):

        if not self.isActive:
            return
        row = {
            'identifier': self.__class__.__name__,
            **data,
        }
        queue = self.getDBQueue(self['timeLogDB'])
        queue.put(row)

    def timeLogReport(self, identifier: str = None, tag: str = None,
                      parentTag: str = None,
                      minJiff: str | datetime.datetime = None, maxJiff: str | datetime.datetime = None,
                      groupBy=None, **kwArgs) -> list[dict]:
        if not self.isActive:
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

        if parentTag is not None:
            qpT = pipes.any(qpT, pipes=[
                ('equals', {'map': {'tagPath': f"{ parentTag }"}}),
                ('equals', {'map': {'tagPath': f"%/{ parentTag }"}, 'op': 'LIKE'})
            ])

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

        rows = db.query(qpT, **kwArgs)

        return rows
