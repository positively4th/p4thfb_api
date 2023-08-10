import unittest
import random
import asyncio
from time import time
from time import sleep
from tempfile import gettempdir
import os
import ramda as R
import datetime
import time

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpydb.db.sqlite.db_async import DB

from src.mixins.timelogdb import TimeLogDB
from src.store.store import Store
from src.store.queue.queueitem import QueueItem


class TestTimeLog(unittest.IsolatedAsyncioTestCase):

    random.seed()

    @classmethod
    def uniqueDBName(cls):
        return '{}{}{}.{}.{}'.format(gettempdir(),
                                     os.path.sep, os.path.basename(__file__), time.time(), random.randint(0, 10000000))

    async def test_decorator(self):

        db = DB(fileName=self.uniqueDBName())

        def sleeper(dt: float):
            res = dt * 2
            sleep(res)
            return res

        timeLogDBee = As(TimeLogDB)({
            'timeLogDB': db,
        })

        t0 = datetime.datetime.now()
        sum = 0
        sum += await timeLogDBee.asRuntimeLogged(sleeper,
                                                 identifier='sleeper', tag='first', group='A', count=1)(0.1)
        sum += await timeLogDBee.asRuntimeLogged(sleeper,
                                                 identifier='sleeper', tag='second', group='A', count=1)(0.2)
        sum += await timeLogDBee.asRuntimeLogged(sleeper,
                                                 identifier='sleeper', tag='third', group='B', count=1)(0.3)
        t1 = datetime.datetime.now()

        while timeLogDBee.pendingRows > 0:
            await asyncio.sleep(0.1)

        self.assertAlmostEqual(2*0.6, sum, places=5)

        rows = await timeLogDBee.timeLogReport(minJiff=t1, maxJiff=t0)
        self.assertEquals(0, len(rows))

        rows = await timeLogDBee.timeLogReport(minJiff=t0, maxJiff=t1)
        print(rows)
        self.assertEquals(3, len(rows))
        rows = R.sort(lambda r1, r2: -1 if r1['jiff'] < r2['jiff']
                      else (1 if r1['jiff'] > r2['jiff'] else 0))(rows)
        self.assertAlmostEqual(2*0.1, rows[0]['elapsed'], places=2)
        self.assertAlmostEqual(2*0.2, rows[1]['elapsed'], places=2)
        self.assertAlmostEqual(2*0.3, rows[2]['elapsed'], places=2)


if __name__ == '__main__':

    unittest.main()
