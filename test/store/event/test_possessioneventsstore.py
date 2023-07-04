import unittest
import testing.postgresql
import subprocess
import ramda as R

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thpydb.db.pgsql.db_async import DB

from src.store.event.possessioneventsstore import PossessionEventsStore
from src.mappers.event.possessioneventsmapper_v2 import PossessionEventsMapper

from src.store.autostores import setAutoStoresDBs


class TestPossessionEventsStore(unittest.IsolatedAsyncioTestCase):

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

    async def test_one(self):

        db = DB(self.db.url())

        storee = As(PossessionEventsStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 3000
        })

        possession__id = await storee.possession__id(
            {'file': '3788743', 'possession': 3})
        possessionEvents = await storee.get(possession__id)
        self.assertIsNotNone(possessionEvents)
        self.assertEqual(19, len(possessionEvents))
        possessionEvents = R.sort_by(
            lambda e: int(e['index']))(possessionEvents)
        self.assertEqual(
            len(possessionEvents)-1, possessionEvents[18]['index'] - possessionEvents[0]['index'])
        possessionEvents = R.for_each(
            lambda e: self.assertAlmostEqual(3, e['possession']))(possessionEvents)
        possessionEvents = R.for_each(
            lambda e: self.assertAlmostEqual(possession__id, e['possession__id']))(possessionEvents)

    async def test_byEvent(self):

        db = DB(self.db.url())

        storee = As(PossessionEventsStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 1
        })

        event__id = '8280443574150717854'  # 8e1278b5-7c84-4eb2-b9f4-bdd0b441c19e
        possession__id = await PossessionEventsMapper.possession__id(
            db, {'file': '3788743', 'possession': 3})
        possessionEvents = await storee.byEvent(event__id)
        self.assertIsNotNone(possessionEvents)
        self.assertEqual(19, len(possessionEvents))
        possessionEvents = R.sort_by(
            lambda e: int(e['index']))(possessionEvents)
        self.assertEqual(
            len(possessionEvents)-1, possessionEvents[18]['index'] - possessionEvents[0]['index'])
        R.for_each(
            lambda e: self.assertAlmostEqual(3, e['possession']))(possessionEvents)
        R.for_each(
            lambda e: self.assertAlmostEqual(possession__id, e['possession__id']))(possessionEvents)


if __name__ == '__main__':

    unittest.main()
