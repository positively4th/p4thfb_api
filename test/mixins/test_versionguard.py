import unittest
import numpy as np
import ramda as R
from json import dumps

from contrib.pyas.src.pyas_v3 import As
from contrib.pyas.src.pyas_v3 import Leaf
from contrib.p4thpymap.src.reducers.logical import all
from contrib.p4thpymap.src.reducers.logical import any

from src.mixins.versionguard import globalVersionGuard
from src.mixins.versionguard import VersionGuardMismatchError

VersionGuard = globalVersionGuard()


class VersionGuardTest(unittest.TestCase):

    def test_ScalarEqual(self):

        class VersionGuardLeaf(Leaf):

            testDomainVersionMap = {}

            prototypes = [VersionGuard] + VersionGuard.prototypes

            @classmethod
            def getDomainVersionMap(cls, *arg, ** kwargs):
                return cls.testDomainVersionMap

        specs = [
            {
                'approvedVersions': {
                    'app': '==0.9.9',
                },
                'domainVersionMap': {
                    'app': '1.0.0'
                },
                'expected': {'app': False}
            },
            {
                'approvedVersions': {
                    'app': '==1.0.0',
                },
                'domainVersionMap': {
                    'app': '1.0.0'
                },
                'expected': {'app': True}
            },
            {
                'approvedVersions': {
                    'app': '==1.0.1',
                },
                'domainVersionMap': {
                    'app': '1.0.0'
                },
                'expected': {'app': False}
            },
            {
                'approvedVersions': {
                    'app': '==1.1.0',
                },
                'domainVersionMap': {
                    'app': '1.0.0'
                },
                'expected': {'app': False}
            },
            {
                'approvedVersions': {
                    'app': '==2.0.0',
                },
                'domainVersionMap': {
                    'app': '1.0.0'
                },
                'expected': {'app': False}
            },
        ]

        for spec in specs:
            VersionGuardLeaf.testDomainVersionMap = spec['domainVersionMap']
            VersionGuardLeaf.approvedVersions = spec['approvedVersions']
            VersionGuardLeaf.allowUnapprovedVersion = True
            versionApproveLeafee = As(VersionGuardLeaf, noCache=True)()

            self.assertEquals(
                spec['expected'], versionApproveLeafee.checkVersions(), spec['approvedVersions']['app'])

            if R.find(lambda domain: spec['expected'][domain] is False)(spec['expected']):
                with self.assertRaises(VersionGuardMismatchError):
                    VersionGuardLeaf.allowUnapprovedVersion = False
                    As(VersionGuardLeaf, noCache=True)()

            else:
                VersionGuardLeaf.allowUnapprovedVersion = True
                As(VersionGuardLeaf, noCache=True)()

    def test_ScalarRange(self):

        class VersionGuardLeaf2(Leaf):

            testDomainVersionMap = {}
            prototypes = [VersionGuard] + VersionGuard.prototypes

            @classmethod
            def getDomainVersionMap(cls, *arg, ** kwargs):
                return cls.testDomainVersionMap

        specs = [
            {
                'approvedVersions': {
                    'app': ['>=0.9.9', '<=1.0.1'],
                },
                'domainVersionMap': {
                    'app': '0.9.8'
                },
                'expected': {'app': False}
            },
            {
                'approvedVersions': {
                    'app': ['>=0.9.9', '<=1.0.1'],
                },
                'domainVersionMap': {
                    'app': '0.9.9'
                },
                'expected': {'app': True}
            },
            {
                'approvedVersions': {
                    'app': ['>=0.9.9', '<=1.0.1'],
                },
                'domainVersionMap': {
                    'app': '1.0.1'
                },
                'expected': {'app': True}
            },
            {
                'approvedVersions': {
                    'app': ['>=0.9.9', '<=1.0.1'],
                },
                'domainVersionMap': {
                    'app': '1.0.2'
                },
                'expected': {'app': False}
            },
        ]

        for spec in specs:
            VersionGuardLeaf2.testDomainVersionMap = spec['domainVersionMap']
            VersionGuardLeaf2.approvedVersions = spec['approvedVersions']
            VersionGuardLeaf2.allowUnapprovedVersion = True
            versionApproveLeafee = As(VersionGuardLeaf2, noCache=True)()

            self.assertEquals(
                spec['expected'],
                versionApproveLeafee.checkVersions(),
                (
                    spec['approvedVersions']['app'],
                    spec['domainVersionMap']
                )
            )

    def test_Vector(self):

        class VersionGuardVector(Leaf):

            testDomainVersionMap = {}
            prototypes = [VersionGuard] + VersionGuard.prototypes

            @classmethod
            def getDomainVersionMap(cls, *arg, ** kwargs):
                return cls.testDomainVersionMap

        specs = [
            {
                'domainVersionMap': {
                    'section1': '1.0.0',
                    'section2': '1.0.0',
                    'section3': '1.0.0',
                },
                'approvedVersions': {
                    'section1': ['>=0.9.9', '<=1.0.1'],
                    'section2': ['>=0.9.9', '<=1.0.1'],
                    'section3': ['>=0.9.9', '<=1.0.1'],
                },
                'expected': {
                    'section1': True,
                    'section2': True,
                    'section3': True,
                }
            },
            {
                'domainVersionMap': {
                    'section1': '2.0.0',
                    'section2': '2.0.0',
                    'section3': '2.0.0',
                },
                'approvedVersions': {
                    'section1': ['>=0.9.9', '<=1.0.1'],
                    'section2': ['>=0.9.9', '<=1.0.1'],
                    'section3': ['>=0.9.9', '<=1.0.1'],
                },
                'expected': {
                    'section1': False,
                    'section2': False,
                    'section3': False,
                }
            },
            {
                'domainVersionMap': {
                    'section1': '1.0.0',
                    'section2': '2.0.0',
                    'section3': '1.0.0',
                },
                'approvedVersions': {
                    'section1': ['>=0.9.9', '<=1.0.1'],
                    'section2': ['>=0.9.9', '<=1.0.1'],
                    'section3': ['>=0.9.9', '<=1.0.1'],
                },
                'expected': {
                    'section1': True,
                    'section2': False,
                    'section3': True,
                }
            },
            {
                'domainVersionMap': {
                    'section1': '1.0.0',
                    'section3': '1.0.0',
                },
                'approvedVersions': {
                    'section1': ['>=0.9.9', '<=1.0.1'],
                    'section2': ['>=0.9.9', '<=1.0.1'],
                    'section3': ['>=0.9.9', '<=1.0.1'],
                },
                'expected': {
                    'section1': True,
                    'section2': None,
                    'section3': True,
                }
            },
        ]

        def reallyTrue(val: bool | None): return val is True
        def reallyFalse(val: bool | None): return val is False

        for i, spec in enumerate(specs):
            label = 'spec {}. json: {}'.format(str(i), dumps(spec))
            VersionGuardVector.testDomainVersionMap = spec['domainVersionMap']
            VersionGuardVector.approvedVersions = spec['approvedVersions']
            VersionGuardVector.allowUnapprovedVersion = True
            VersionGuardVectoree = As(VersionGuardVector, noCache=True)()

            self.assertEquals(
                spec['expected'],
                VersionGuardVectoree.checkVersions(), label
            )

            anyFalse = any(spec['expected'], reallyFalse)

            self.assertEqual(
                not anyFalse, VersionGuardVectoree.areVersionsOk(), label)

            if anyFalse:
                with self.assertRaises(VersionGuardMismatchError):
                    VersionGuardVectoree.verifyVersions()
            else:
                VersionGuardVectoree.verifyVersions()


if __name__ == '__main__':

    unittest.main()
