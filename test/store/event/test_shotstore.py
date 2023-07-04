import unittest
import subprocess
from time import time
import testing.postgresql

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thpydb.db.pgsql.db_async import DB

from src.store.event.type.shotstore import ShotStore


class TestShotStore(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):

        cls.db = testing.postgresql.Postgresql()
        subprocess.run([
            'psql',
            cls.db.url(),
            '-f', './test/data/3788743_3795187_v2/db.sql'
        ])

    @classmethod
    def tearDownClass(cls):
        cls.db.stop()

    async def timer(self, f, *args, **kwargs):
        t0 = time()
        res = await f(*args, **kwargs)
        t1 = time()
        return res, t1 - t0

    async def test_one(self):

        db = DB(self.db.url())
        store = As(ShotStore)({
            'db': db,
            'batchDelay': 1.0,
            'batchSize': 2
        })
        # event 6089ad85-71f8-4e3f-a46b-8c3351f44cfe -> shot
        res = self.timer(store.get, '9473833955833613912')
        res, dt = await res
        res = res[0]
        self.assertEquals('9473833955833613912', res['__id'])
        self.assertGreater(dt, 1.0)
        res, dt = await self.timer(store.get, '9473833955833613912')
        res = res[0]
        self.assertEquals('9473833955833613912', res['__id'])
        self.assertLess(dt, 1.0)

    async def test_byEvent(self):

        db = DB(self.db.url())
        storee = As(ShotStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 3
        })

        # event 6089ad85-71f8-4e3f-a46b-8c3351f44cfe -> shot
        shot = await storee.byEvent('9286411016168614669')
        self.assertEquals('9286411016168614669', shot['event__id'])
        self.assertEquals('9473833955833613912', shot['__id'])


if __name__ == '__main__':

    unittest.main()
