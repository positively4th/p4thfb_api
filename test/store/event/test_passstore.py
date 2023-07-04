import unittest
from time import time
import testing.postgresql
import subprocess

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thpydb.db.pgsql.db_async import DB

from src.store.event.type.passstore import PassStore
from src.store.autostores import setAutoStoresDBs


class TestPassStore(unittest.IsolatedAsyncioTestCase):

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

    async def timer(self, f, *args, **kwargs):
        t0 = time()
        res = await f(*args, **kwargs)
        t1 = time()
        return res, t1 - t0

    async def test_one(self):

        db = DB(self.db.url())
        store = As(PassStore)({
            'db': db,
            'batchDelay': 1.0,
            'batchSize': 2
        })

        event__id = '13925197567206837852'
        pass__id = '15045540176389843616'
        res, dt = await self.timer(store.get, pass__id)
        res = res[0]
        self.assertGreater(dt, 1.0)
        self.assertIsNotNone(res)
        self.assertEqual(pass__id, res['__id'])
        self.assertEqual(event__id, res['event__id'])
        self.assertAlmostEqual(13.917615, res['length'], delta=0.00001)

        res, dt = await self.timer(store.get, pass__id)
        res = res[0]
        self.assertLess(dt, 1.0)
        self.assertEqual(pass__id, res['__id'])
        self.assertEqual(event__id, res['event__id'])

    async def test_byEvent(self):

        db = DB(self.db.url())

        storee = As(PassStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 3
        })
        event__id = '13925197567206837852'
        pass__id = '15045540176389843616'

        _pass = await storee.byEvent(event__id)
        self.assertEquals(pass__id, _pass['__id'])
        self.assertEquals(event__id, _pass['event__id'])


if __name__ == '__main__':

    unittest.main()
