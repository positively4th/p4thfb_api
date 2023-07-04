import unittest
from time import time
import testing.postgresql
import subprocess

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thpydb.db.pgsql.db_async import DB

from src.store.event.eventstore import EventStore
from src.store.autostores import setAutoStoresDBs


class TestEventStore(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):

        cls.db = testing.postgresql.Postgresql()
        subprocess.run([
            'psql',
            cls.db.url(),
            '-f', './test/data/3788743_3795187_v2/db.sql'
        ])
        setAutoStoresDBs(DB(cls.db.url()))

    @classmethod
    def tearDownClass(cls):
        cls.db.stop()

    async def timer(f, *args, **kwargs):
        t0 = time()
        res = await f(*args, **kwargs)
        t1 = time()
        return res, t1 - t0

    async def test_one(self):

        store = As(EventStore)({
            'db': DB(self.db.url()),
            'batchDelay': 0.1,
            'batchSize': 2
        })

        res, dt = await TestEventStore.timer(store.get, '10000030782764428682')
        self.assertGreater(dt, 0.1)
        res, dt = await TestEventStore.timer(store.get, '10000030782764428682')
        self.assertLess(dt, 1.0)


if __name__ == '__main__':

    unittest.main()
