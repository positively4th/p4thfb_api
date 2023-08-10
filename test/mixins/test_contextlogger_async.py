import unittest
import random
import asyncio
from time import time
import os
import time
from tempfile import mkdtemp
from contrib.pyas.src.pyas_v3 import As
from contrib.p4thpydb.db.sqlite.db import DB as syncDB
from inspect import isawaitable

from src.mixins.contextlogger import ContextLogger


class TestContextLoggerAsync(unittest.IsolatedAsyncioTestCase):

    random.seed()

    @staticmethod
    def createCounter():

        ctr = -1

        def helper():

            nonlocal ctr

            ctr += 1
            return ctr

        return helper

    @staticmethod
    async def cpuWork(seconds: float, f: callable = None):

        t0 = time.time()
        count = 0
        while count % 10000 != 0 or time.time() < (t0 + seconds):
            count += 1

        res = 'cpuWork'
        if f:
            res = await f(res)
        return res

    @staticmethod
    async def systemWork(seconds: float, f: callable = None):

        t0 = time.time()
        t1 = t0 + seconds
        while time.time() < t1:
            pass

        res = 'systemWork'
        if f:
            res = await f(res)
        return res

    @staticmethod
    async def asyncSleep(seconds: float, f: callable = None):

        await asyncio.sleep(seconds)

        res = 'asyncSleep'
        if f:
            res = await f(res)
        return res

    async def test_iterative(self):

        dbFile = os.path.join(mkdtemp(), str(time.time()))
        # dbFile = ':memory:'
        db = syncDB(fileName=dbFile)
        print('dbFile: ', dbFile)

        specs = [
            {
                'expElapsed': 0.1,
                'expUser': 0.1,
                'expSystem': 0.0,
                'f': self.cpuWork,
                'tolerance': 0.2,
            },
            {
                'expElapsed': 1,
                'expUser': 0.0,
                'expSystem': 0.0,
                'f': self.asyncSleep,
                'tolerance': 0.2,
                'kwArgs': {
                    'tag': 'ASYNCSLEEP'
                }
            },
            {
                'expElapsed': 1,
                'expUser': 0.0,
                'expSystem': 0.0,
                'f': self.asyncSleep,
                'tolerance': 0.20,
            },
            {
                'expElapsed': 1,
                'expUser': 0.0,
                'expSystem': 1,
                'f': self.systemWork,
                'tolerance': 0.20,
            },
        ]

        async def run(spec):

            kwArgs = {
                'resultHandler': ContextLogger.noResultHandler,
            }

            if 'kwArgs' in spec:
                kwArgs.update(spec['kwArgs'])

            return await ContextLogger.asLogged(
                spec['f'],
                **kwArgs
            )(spec['expElapsed'])

        contextLogger = As(ContextLogger)({
            'timeLogDB': db,
            'staticData': {
                'identifier': 'id1'
            }
        })
        ContextLogger.setContextLogger(contextLogger)

        for i, spec in enumerate(specs):

            res = await ContextLogger.asLogged(run)(spec)

            if isawaitable(res):
                res = await res

            while contextLogger.isPending:
                await asyncio.sleep(0.1)

            id = contextLogger['staticData']['identifier']

            tag = spec['f'].__name__
            if 'kwArgs' in spec and 'tag' in spec['kwArgs']:
                tag = spec['kwArgs']['tag']
            rows = contextLogger.timeLogReport(fetchAll=True)
            rows = contextLogger.timeLogReport(
                identifier=id, tag=tag, fetchAll=True)
            self.assertEquals(1, len(rows), msg=str(i)+tag)
            # print(rows[0])
            delta = spec['tolerance'] * abs(spec['expElapsed'])
            self.assertEquals('', rows[0]['error'], msg=str(i)+tag)
            self.assertAlmostEqual(
                spec['expElapsed'], rows[0]['elapsed'], delta=delta, msg=str(i)+tag)
            self.assertAlmostEqual(
                spec['expUser'], rows[0]['user'], delta=delta, msg=str(i)+tag)
            self.assertAlmostEqual(
                spec['expSystem'], rows[0]['system'], delta=delta, msg=str(i)+tag)

    async def test_recursive(self):

        dbFile = os.path.join(mkdtemp(), str(time.time()))
        # dbFile = ':memory:'
        db = syncDB(fileName=dbFile)
        print('dbFile: ', dbFile)

        counter = self.createCounter()

        specs = [
            {
                'expElapsed': 1,
                'expUser': 0.0,
                'expSystem': 1,
                'f': self.systemWork,
                'tolerance': 0.20,
                'kwArgs': {
                    'tag': self.systemWork.__name__ + str(counter())
                }
            },
            {
                'expElapsed': 1,
                'expUser': 1.0,
                'expSystem': 0.0,
                'f': self.cpuWork,
                'tolerance': 0.2,
                'kwArgs': {
                    'tag': self.cpuWork.__name__ + str(counter())
                }
            },
        ]

        contextLogger = As(ContextLogger)({
            'timeLogDB': db,
            'staticData': {
                'identifier': 'id1'
            }
        })
        ContextLogger.setContextLogger(contextLogger)

        # while contextLogger.isPending:
        await asyncio.sleep(0.1)

        async def run(specs, res=None):

            spec = specs.pop(0)

            async def wrapper(res):
                return await run(specs, res)

            kwArgs = {
                'doAwait': True,
                'resultHandler': ContextLogger.noResultHandler,
            }

            if 'kwArgs' in spec:
                kwArgs.update(spec['kwArgs'])

            args = [spec['expElapsed']]
            if len(specs) > 0:
                args.append(wrapper)

            res = await ContextLogger.asLogged(
                spec['f'],
                **kwArgs
            )(*args)
            return res

        await ContextLogger.asLogged(run)(list(specs))
        await asyncio.sleep(1.1)

        rows = contextLogger.timeLogReport(fetchAll=True)
        self.assertEquals(1+len(specs), len(rows))

        totDelta = 0
        expTotElapsed = 0
        expTotUser = 0
        expTotSystem = 0

        msg = []
        for i in reversed(range(len(specs))):

            spec = specs[i]

            totDelta += abs(spec['expElapsed'] * spec['tolerance'])
            expTotElapsed += spec['expElapsed']
            expTotUser += spec['expUser']
            expTotSystem += spec['expSystem']

            tag = spec['f'].__name__

            parentSpec = specs[i-1] if i > 0 else {}
            parentTag = parentSpec['f'].__name__ if 'f' in parentSpec else 'run'

            if 'kwArgs' in spec and 'tag' in spec['kwArgs']:
                tag = spec['kwArgs']['tag']

            if 'kwArgs' in parentSpec and 'tag' in parentSpec['kwArgs']:
                parentTag = parentSpec['kwArgs']['tag']

            contextLogger = contextLogger
            if 'contextLogger' in spec:
                contextLogger = spec['contextLogger']

            id = contextLogger['staticData']['identifier']

            msg.insert(0, tag)

            rows = contextLogger.timeLogReport(
                identifier=id, tag=tag, parentTag=parentTag, fetchAll=True)
            self.assertEquals(1, len(rows))

            delta = totDelta
            self.assertEquals('', rows[0]['error'], msg=tag)
            self.assertAlmostEqual(
                expTotElapsed, rows[0]['elapsed'], delta=delta, msg='->'.join(msg))
            self.assertAlmostEqual(
                expTotUser, rows[0]['user'], delta=delta, msg='->'.join(msg))
            self.assertAlmostEqual(
                expTotSystem, rows[0]['system'], delta=delta, msg='->'.join(msg))

        rows = contextLogger.timeLogReport(tag='run', fetchAll=True)
        self.assertEquals(1, len(rows))
        self.assertAlmostEqual(
            expTotElapsed, rows[0]['elapsed'], delta=totDelta, msg='run')
        self.assertAlmostEqual(
            expTotUser, rows[0]['user'], delta=totDelta, msg='run')
        self.assertAlmostEqual(
            expTotSystem, rows[0]['system'], delta=totDelta, msg='run')

        # print(rows[0])

        # del contextLogger0


if __name__ == '__main__':

    unittest.main()
