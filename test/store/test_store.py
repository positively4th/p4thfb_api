import unittest
import testing.postgresql
import subprocess

from contrib.p4thpydb.db.pgsql.db_async import DB

from src.store.autostores import getAutoStores
from src.store.autostores import setAutoStoresDBs


class TestStore(unittest.IsolatedAsyncioTestCase):

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

    async def test_AutoStore(self):

        db = DB(self.db.url())

        setAutoStoresDBs(db)
        autoStores = getAutoStores()

        shotStoree = autoStores['shotStore']
        shot = await shotStoree.byEvent('8946741018004882275')
        self.assertEquals('8946741018004882275', shot['event__id'])


if __name__ == '__main__':

    unittest.main()
