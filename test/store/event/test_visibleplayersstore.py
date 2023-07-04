import unittest
from time import time
import testing.postgresql
import subprocess
import ramda as R

from contrib.pyas.src.pyas_v3 import As

from contrib.p4thpydb.db.pgsql.db_async import DB


from src.store.visibleplayersstore import VisiblePlayersStore


class TestVisiblePlayersStore(unittest.IsolatedAsyncioTestCase):

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
        store = As(VisiblePlayersStore)({
            'db': db,
            'batchDelay': 1.0,
            'batchSize': 2
        })

        event__id = '1749248788999781745'
        eventId = '88faaa20-9709-47dc-aad6-9585ae2ada4b'
        threesixty__id = '7837155533815336422'

        res, dt = await self.timer(store.get, threesixty__id)
        self.assertGreater(dt, 1.0)
        self.assertEqual(19, len(res))
        actors = R.filter(lambda vp: vp['actor'])(res)
        self.assertEqual(1, len(actors))
        self.assertAlmostEqual(91.038, actors[0]['x'], delta=0.00001)
        self.assertAlmostEqual(67.6181, actors[0]['y'], delta=0.00001)

        res, dt = await self.timer(store.get, threesixty__id)
        self.assertLess(dt, 1.0)
        self.assertEqual(19, len(res))
        actors = R.filter(lambda vp: vp['actor'])(res)
        self.assertEqual(1, len(actors))
        self.assertAlmostEqual(91.038, actors[0]['x'], delta=0.00001)
        self.assertAlmostEqual(67.6181, actors[0]['y'], delta=0.00001)

    async def test_byEvent(self):

        db = DB(self.db.url())

        storee = As(VisiblePlayersStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 3
        })

        event__id = '1749248788999781745'
        eventId = '88faaa20-9709-47dc-aad6-9585ae2ada4b'
        threesixty__id = '7837155533815336422'
        vps = await storee.byEvent(event__id)
        self.assertEqual(19, len(vps))
        for vp in vps:
            self.assertEquals(event__id, vp['event__id'])
            self.assertEquals(threesixty__id, vp['__id'])

        self.assertEqual(19, len(R.filter(
            lambda vp: vp['__id'] == threesixty__id)(vps)))


if __name__ == '__main__':

    unittest.main()
