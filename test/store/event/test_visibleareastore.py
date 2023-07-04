import unittest
from time import time
import testing.postgresql
import subprocess
import ramda as R

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thpydb.db.pgsql.db_async import DB

from src.store.visibleareastore import VisibleAreaStore


class TestVisibleAreaStore(unittest.IsolatedAsyncioTestCase):

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
        store = As(VisibleAreaStore)({
            'db': db,
            'batchDelay': 1.0,
            'batchSize': 2
        })

        # event db94f940-a571-4f2f-8891-3c04163e3287 (2953126156637834812)
        # threesixty.__id "5863369953294641332"
        va__id = "5863369953294641332"
        res, dt = await self.timer(store.get, va__id)
        self.assertGreater(dt, 1.0)
        self.assertEqual(7, len(res))
        self.assertEqual(va__id, res[0]['__id'])

        res, dt = await self.timer(store.get, va__id)
        self.assertLess(dt, 1.0)
        self.assertEqual(7, len(res))
        self.assertEqual(va__id, res[0]['__id'])

    async def test_byEvent(self):

        db = DB(self.db.url())

        storee = As(VisibleAreaStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 3
        })

        # event db94f940-a571-4f2f-8891-3c04163e3287 (2953126156637834812)
        # threesixty.__id "5863369953294641332"
        vas = (await storee.byEvent('2953126156637834812'))
        self.assertEqual(7, len(vas))
        for va in vas:
            self.assertEquals('2953126156637834812', va['event__id'])

        self.assertEqual(7, len(R.filter(
            lambda va: va['__id'] == '5863369953294641332')(vas)))


if __name__ == '__main__':

    unittest.main()
