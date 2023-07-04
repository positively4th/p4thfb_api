import unittest
import ramda as R
import testing.postgresql
import subprocess

from contrib.pyas.src.pyas_v3 import As
from contrib.p4thpydb.db.pgsql.db_async import DB

from src.store.event.eventstore import EventStore
from src.store.autostores import setAutoStoresDBs
from src.mixins.event.event_v2 import Event
from src.mappers.event.constants import Constants
from src.mappers.event.possessioneventsmapper_v2 import PossessionEventsMapper


class TestEvent(unittest.IsolatedAsyncioTestCase):

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

        store = As(EventStore)({
            'db': db,
            'batchDelay': 0.01,
            'batchSize': 50
        })

        event = (await store.get('15320185092885708205'))[0]
        eventee = As(Event)(event)
        self.assertEqual('15320185092885708205', eventee['__id'])
        self.assertEqual(1, eventee['index'])
        self.assertEqual(1, eventee['possession'])

    async def test_shot(self):

        db = DB(self.db.url())

        eventStore = As(EventStore)({
            'db': db,
            'batchDelay': 0.01,
            'batchSize': 1
        })

        event = {
            **(await eventStore.get('2953126156637834812'))[0]
        }
        eventee = As(Event)(event)
        self.assertEqual('2953126156637834812', eventee['__id'])
        self.assertEqual(Constants.shotTypeId, eventee['typeId'])

        shot = await eventee['type']
        self.assertIsNotNone(shot)
        self.assertAlmostEqual(
            0.014329195, shot['xG'], delta=0.00001)

    async def test_pass(self):

        db = DB(self.db.url())

        eventStore = As(EventStore)({
            'db': db,
            'batchDelay': 0.01,
            'batchSize': 1
        })

        event = {
            **(await eventStore.get('13925197567206837852'))[0]
        }
        eventee = As(Event)(event)
        self.assertEqual('13925197567206837852', eventee['__id'])
        self.assertEqual(Constants.passTypeId, eventee['typeId'])

        _pass = await eventee['type']
        self.assertIsNotNone(_pass)
        self.assertEqual('15045540176389843616', _pass['__id'])
        self.assertAlmostEqual(
            13.917615, _pass['length'], delta=0.00001)

    async def test_visibleArea(self):

        db = DB(self.db.url())

        eventStore = As(EventStore)({
            'db': db,
            'batchDelay': 0.01,
            'batchSize': 1
        })

        event = {
            **(await eventStore.get('1749248788999781745'))[0]
        }
        eventee = As(Event)(event)
        self.assertEqual('1749248788999781745', eventee['__id'])

        va = await eventee['visibleArea']
        self.assertIsNotNone(va)
        self.assertEqual(5, len(va))
        va0 = R.find(lambda va: va['index'] == 0)(va)
        self.assertAlmostEqual(48.4706784790806, va0['x'], delta=0.001)
        self.assertAlmostEqual(80.0, va0['y'], delta=0.001)

        va4 = R.find(lambda va: va['index'] == 4)(va)
        self.assertEqual(va0['x'], va4['x'])
        self.assertEqual(va0['y'], va4['y'])

    async def test_visiblePlayers(self):

        db = DB(self.db.url())

        eventStore = As(EventStore)({
            'db': db,
            'batchDelay': 0.01,
            'batchSize': 1
        })

        event = {
            **(await eventStore.get('1749248788999781745'))[0]
        }
        eventee = As(Event)(event)
        self.assertEqual('1749248788999781745', eventee['__id'])

        vps = await eventee['visiblePlayers']
        self.assertIsNotNone(vps)
        self.assertEqual(19, len(vps))
        actor = R.find(lambda vp: vp['actor'])(vps)
        self.assertIsNotNone(actor)
        self.assertAlmostEqual(91.038, actor['x'], places=3)
        self.assertAlmostEqual(67.6181, actor['y'], places=3)

    async def test_relatedEvents(self):

        db = DB(self.db.url())

        eventStore = As(EventStore)({
            'db': db,
            'batchDelay': 0.01,
            'batchSize': 1
        })

        # event 6089ad85-71f8-4e3f-a46b-8c3351f44cfe -> shot
        event = {
            **(await eventStore.get('9286411016168614669'))[0]
        }
        eventee = As(Event)(event)
        self.assertEqual('9286411016168614669', eventee['__id'])

        res = await eventee['relatedEvents']

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

    async def test_export_1(self):

        db = DB(self.db.url())

        eventStore = As(EventStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 100
        })

        shotEvent = {
            **(await eventStore.get('2953126156637834812'))[0]
        }
        shotEventee = As(Event)(shotEvent)
        self.assertEqual('2953126156637834812', shotEventee['__id'])

        passEvent = {
            **(await eventStore.get('13925197567206837852'))[0]
        }
        passEventee = As(Event)(passEvent)
        self.assertEqual('13925197567206837852', passEventee['__id'])

        visibleAreaEvent = {
            **(await eventStore.get('1749248788999781745'))[0]}
        visibleAreaEventee = As(Event)(visibleAreaEvent)
        self.assertEqual('1749248788999781745', visibleAreaEventee['__id'])

        visiblePlayerEvent = {
            **(await eventStore.get('1749248788999781745'))[0]}
        visiblePlayerEventee = As(Event)(visiblePlayerEvent)
        self.assertEqual('1749248788999781745', visiblePlayerEventee['__id'])

        relatedEventsEvent = {
            # event 5ce4a0f5-c8fd-429b-8b3a-866b01b1681f -> pass
            **(await eventStore.get('13690674646770382944'))[0]}
        relatedEventsEventee = As(Event)(relatedEventsEvent)
        self.assertEqual('13690674646770382944', relatedEventsEventee['__id'])

        possessionEventsEvent = {
            # 8e1278b5-7c84-4eb2-b9f4-bdd0b441c19e
            **(await eventStore.get('8280443574150717854'))[0]}
        possessionEventsEventee = As(Event)(possessionEventsEvent)
        self.assertEqual('8280443574150717854',
                         possessionEventsEventee['__id'])

        act = await Event.export([
            shotEvent,
            passEvent,
            visibleAreaEvent,
            visiblePlayerEvent,
            relatedEventsEvent,
            possessionEventsEvent
        ], features={
            'type': None,
            'visibleArea': None,
            'visiblePlayers': None,
            'relatedEvents': None,
            'possessionEvents': None,
        })
        self.assertEquals(6, len(act))

        # shotEvent
        actShot = act[0]
        self.assertIsNotNone(actShot)
        typeShot = actShot['type']
        self.assertAlmostEqual(
            0.014329195, typeShot['xG'], delta=0.00001)

        # passEvent
        actPass = act[1]
        typePass = actPass['type']
        self.assertIsNotNone(typePass)
        self.assertEqual('15045540176389843616', typePass['__id'])
        self.assertAlmostEqual(
            13.917615, typePass['length'], delta=0.00001)

        visibleAreaEvent
        actVisibleArea = act[2]
        va = actVisibleArea['visibleArea']
        self.assertIsNotNone(va)
        self.assertEqual(5, len(va))
        va0 = R.find(lambda va: va['index'] == 0)(va)
        self.assertAlmostEqual(48.4706784790806, va0['x'], delta=0.001)
        self.assertAlmostEqual(80.0, va0['y'], delta=0.001)

        va4 = R.find(lambda va: va['index'] == 4)(va)
        self.assertEqual(va0['x'], va4['x'])
        self.assertEqual(va0['y'], va4['y'])

        # visiblePlayerEvent
        actVisiblePlayer = act[3]
        vp = actVisiblePlayer['visiblePlayers']
        self.assertIsNotNone(vp)
        self.assertEqual(19, len(vp))
        actor = R.find(lambda vp: vp['actor'])(vp)
        self.assertIsNotNone(actor)
        self.assertAlmostEqual(91.038, actor['x'], places=3)
        self.assertAlmostEqual(67.6181, actor['y'], places=3)

        # relatedEvents
        res = act[4]['relatedEvents']

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

        # possessionEvents
        possessionEvents = act[5]['possessionEvents']
        event__id = '8280443574150717854'  # 8e1278b5-7c84-4eb2-b9f4-bdd0b441c19e
        possession__id = await PossessionEventsMapper.possession__id(
            db, {'file': '3788743', 'possession': 3})
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

    async def test_export_2(self):

        db = DB(self.db.url())

        eventStore = As(EventStore)({
            'db': db,
            'batchDelay': 0.1,
            'batchSize': 100
        })

        shotEvent = {
            **(await eventStore.get('2953126156637834812'))[0]
        }
        shotEventee = As(Event)(shotEvent)
        self.assertEqual('2953126156637834812', shotEventee['__id'])

        passEvent = {
            **(await eventStore.get('13925197567206837852'))[0]
        }
        passEventee = As(Event)(passEvent)
        self.assertEqual('13925197567206837852', passEventee['__id'])

        visibleAreaEvent = {
            **(await eventStore.get('1749248788999781745'))[0]}
        visibleAreaEventee = As(Event)(visibleAreaEvent)
        self.assertEqual('1749248788999781745', visibleAreaEventee['__id'])

        visiblePlayerEvent = {
            **(await eventStore.get('1749248788999781745'))[0]}
        visiblePlayerEventee = As(Event)(visiblePlayerEvent)
        self.assertEqual('1749248788999781745', visiblePlayerEventee['__id'])

        relatedEventsEvent = {
            # event 5ce4a0f5-c8fd-429b-8b3a-866b01b1681f -> pass
            **(await eventStore.get('13690674646770382944'))[0]}
        relatedEventsEventee = As(Event)(relatedEventsEvent)
        self.assertEqual('13690674646770382944', relatedEventsEventee['__id'])

        possessionEventsEvent = {
            # 8e1278b5-7c84-4eb2-b9f4-bdd0b441c19e
            **(await eventStore.get('8280443574150717854'))[0]}
        possessionEventsEventee = As(Event)(possessionEventsEvent)
        self.assertEqual('8280443574150717854',
                         possessionEventsEventee['__id'])

        featuresToExport = {
            'type': None,
            'visibleArea': None,
            'visiblePlayers': None,
            'relatedEvents': {'type': None, 'visibleArea': None, 'visiblePlayers': None, 'relatedEvent': None, 'possessionEvents': None},
            'possessionEvents': {'type': None, 'visibleArea': None, 'visiblePlayers': None, 'relatedEvent': None, 'possessionEvents': None},
        }
        act = await Event.export([
            shotEvent,
            passEvent,
            visibleAreaEvent,
            visiblePlayerEvent,
            relatedEventsEvent,
            possessionEventsEvent
        ], features=featuresToExport)
        self.assertEquals(6, len(act))

        # shotEvent
        actShot = act[0]
        self.assertIsNotNone(actShot)
        typeShot = actShot['type']
        self.assertAlmostEqual(
            0.014329195, typeShot['xG'], delta=0.00001)

        # passEvent
        actPass = act[1]
        typePass = actPass['type']
        self.assertIsNotNone(typePass)
        self.assertEqual('15045540176389843616', typePass['__id'])
        self.assertAlmostEqual(
            13.917615, typePass['length'], delta=0.00001)

        # visibleAreaEvent
        actVisibleArea = act[2]
        va = actVisibleArea['visibleArea']
        self.assertIsNotNone(va)
        self.assertEqual(5, len(va))
        va0 = R.find(lambda va: va['index'] == 0)(va)
        self.assertAlmostEqual(48.4706784790806, va0['x'], delta=0.001)
        self.assertAlmostEqual(80.0, va0['y'], delta=0.001)

        va4 = R.find(lambda va: va['index'] == 4)(va)
        self.assertEqual(va0['x'], va4['x'])
        self.assertEqual(va0['y'], va4['y'])

        # visiblePlayerEvent
        actVisiblePlayer = act[3]
        vp = actVisiblePlayer['visiblePlayers']
        self.assertIsNotNone(vp)
        self.assertEqual(19, len(vp))
        actor = R.find(lambda vp: vp['actor'])(vp)
        self.assertIsNotNone(actor)
        self.assertAlmostEqual(91.038, actor['x'], places=3)
        self.assertAlmostEqual(67.6181, actor['y'], places=3)

        # relatedEvents
        actRelatedEvent = act[4]
        res = actRelatedEvent['relatedEvents']

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

        # possessionEvents
        possessionEvents = act[5]['possessionEvents']
        event__id = '8280443574150717854'  # 8e1278b5-7c84-4eb2-b9f4-bdd0b441c19e
        possession__id = await PossessionEventsMapper.possession__id(
            db, {'file': '3788743', 'possession': 3})
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


if __name__ == '__main__':

    unittest.main()
