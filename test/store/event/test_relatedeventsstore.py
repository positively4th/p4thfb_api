import unittest
from time import time
import testing.postgresql
import subprocess
import ramda as R

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thpydb.db.pgsql.db_async import DB

from src.store.event.relatedeventsstore import RelatedEventsStore
from src.store.autostores import setAutoStoresDBs


class TestRelatedEventsStore(unittest.IsolatedAsyncioTestCase):

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

    async def test_byShotEvent(self):

        db = DB(self.db.url())

        storee = As(RelatedEventsStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 3000
        })

        # event 6089ad85-71f8-4e3f-a46b-8c3351f44cfe -> shot
        res = list((await storee.byEvent('9286411016168614669')).values())

        # shotKeyPass
        re = R.find(lambda e: e['eventId'] ==
                    '5ce4a0f5-c8fd-429b-8b3a-866b01b1681f')(res)
        self.assertIsNotNone(re)
        self.assertIn('shotKeyPass', re['tag'])

        # shotKeyPass
        sares = R.filter(lambda e: 'shotAssisted' in e['tag'])(res)
        self.assertEqual(0, len(sares))

        # related
        re = R.find(lambda e: e['eventId'] ==
                    '27a3de03-a8b8-4c2c-ab54-c09a393b94dc')(res)
        self.assertIsNotNone(re)
        self.assertIn('related', re['tag'])

        re = R.find(lambda e: e['eventId'] ==
                    'f59ec6aa-2759-4078-940e-f77914cc7c77')(res)
        self.assertIsNotNone(re)
        self.assertIn('related', re['tag'])

        # withinPossession
        pres = set(R.pipe(
            R.filter(lambda e: 'withinPossession' in e['tag']),
            R.map(lambda e: e['eventId'])
        )(res))
        self.assertCountEqual([
            "5ce4a0f5-c8fd-429b-8b3a-866b01b1681f",
            "974e9315-5d87-448a-9ad0-0ff8c87bd61e",
            "27a3de03-a8b8-4c2c-ab54-c09a393b94dc",
            "6089ad85-71f8-4e3f-a46b-8c3351f44cfe",
        ], pres)

        # possessionFirst
        pfre = R.pipe(
            R.filter(lambda e: 'possessionFirst' in e['tag']),
            R.map(lambda e: e['eventId'])
        )(res)
        self.assertCountEqual([
            "5ce4a0f5-c8fd-429b-8b3a-866b01b1681f",
        ], pfre)

        # possessionLast
        plre = R.pipe(
            R.filter(lambda e: 'possessionLast' in e['tag']),
            R.map(lambda e: e['eventId'])
        )(res)
        self.assertCountEqual([
            "6089ad85-71f8-4e3f-a46b-8c3351f44cfe",
        ], plre)

    async def test_byShotEvent(self):

        db = DB(self.db.url())

        storee = As(RelatedEventsStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 3000
        })

        # event 6089ad85-71f8-4e3f-a46b-8c3351f44cfe -> shot
        res = (await storee.byEvent('9286411016168614669'))

        # assistingPass
        re = R.find(lambda e: 'assistingPass' in e['tag'])(res)
        self.assertIsNotNone(re)
        self.assertAlmostEqual(
            '5ce4a0f5-c8fd-429b-8b3a-866b01b1681f', re['eventId'])

        # shotAssisted
        sares = R.filter(lambda e: 'shotAssisted' in e['tag'])(res)
        self.assertEqual(0, len(sares))

        # shotKeyPass
        re = R.find(lambda e: e['eventId'] ==
                    '5ce4a0f5-c8fd-429b-8b3a-866b01b1681f')(res)
        self.assertIsNotNone(re)
        self.assertIn('shotKeyPass', re['tag'])

        # related
        re = R.find(lambda e: e['eventId'] ==
                    '27a3de03-a8b8-4c2c-ab54-c09a393b94dc')(res)
        self.assertIsNotNone(re)
        self.assertIn('related', re['tag'])

        re = R.find(lambda e: e['eventId'] ==
                    'f59ec6aa-2759-4078-940e-f77914cc7c77')(res)
        self.assertIsNotNone(re)
        self.assertIn('related', re['tag'])

        # withinPossession
        pres = set(R.pipe(
            R.filter(lambda e: 'withinPossession' in e['tag']),
            R.map(lambda e: e['eventId'])
        )(res))
        self.assertCountEqual([
            "5ce4a0f5-c8fd-429b-8b3a-866b01b1681f",
            "974e9315-5d87-448a-9ad0-0ff8c87bd61e",
            "27a3de03-a8b8-4c2c-ab54-c09a393b94dc",
            "6089ad85-71f8-4e3f-a46b-8c3351f44cfe",
        ], pres)

        # possessionFirst
        pfre = R.pipe(
            R.filter(lambda e: 'possessionFirst' in e['tag']),
            R.map(lambda e: e['eventId'])
        )(res)
        self.assertCountEqual([
            "5ce4a0f5-c8fd-429b-8b3a-866b01b1681f",
        ], pfre)

        # possessionLast
        plre = R.pipe(
            R.filter(lambda e: 'possessionLast' in e['tag']),
            R.map(lambda e: e['eventId'])
        )(res)
        self.assertCountEqual([
            "6089ad85-71f8-4e3f-a46b-8c3351f44cfe",
        ], plre)

    async def test_byPassEvent(self):

        db = DB(self.db.url())

        storee = As(RelatedEventsStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 3000
        })

        # event 5ce4a0f5-c8fd-429b-8b3a-866b01b1681f -> pass
        res = (await storee.byEvent('13690674646770382944'))

        # assistingPass
        re = R.find(lambda e: 'assistingPass' in e['tag'])(res)
        self.assertIsNone(re)

        # shotAssisted
        sares = R.filter(lambda e: 'shotAssisted' in e['tag'])(res)
        self.assertEqual(1, len(sares))
        self.assertEqual(
            '6089ad85-71f8-4e3f-a46b-8c3351f44cfe', sares[0]['eventId'])

        # shotKeyPass
        skpres = R.find(lambda e: 'shotKeyPass' in e['tag'])(res)
        self.assertIsNone(skpres)

        # related
        rs = R.filter(lambda e: 'related' in e['tag'])(res)
        self.assertEquals(1, len(rs))
        re = R.find(lambda e: e['eventId'] ==
                    '974e9315-5d87-448a-9ad0-0ff8c87bd61e')(res)
        self.assertIsNotNone(re)
        self.assertIn('related', re['tag'])

        # withinPossession
        pres = set(R.pipe(
            R.filter(lambda e: 'withinPossession' in e['tag']),
            R.map(lambda e: e['eventId'])
        )(res))
        self.assertCountEqual([
            "5ce4a0f5-c8fd-429b-8b3a-866b01b1681f",
            "974e9315-5d87-448a-9ad0-0ff8c87bd61e",
            "27a3de03-a8b8-4c2c-ab54-c09a393b94dc",
            "6089ad85-71f8-4e3f-a46b-8c3351f44cfe",
        ], pres)

        # possessionFirst
        pfre = R.pipe(
            R.filter(lambda e: 'possessionFirst' in e['tag']),
            R.map(lambda e: e['eventId'])
        )(res)
        self.assertCountEqual([
            "5ce4a0f5-c8fd-429b-8b3a-866b01b1681f",
        ], pfre)

        # possessionLast
        plre = R.pipe(
            R.filter(lambda e: 'possessionLast' in e['tag']),
            R.map(lambda e: e['eventId'])
        )(res)
        self.assertCountEqual([
            "6089ad85-71f8-4e3f-a46b-8c3351f44cfe",
        ], plre)


if __name__ == '__main__':

    unittest.main()
