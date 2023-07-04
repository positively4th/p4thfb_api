from semver import match
from collections.abc import Iterable
import ramda as R
import logging

from contrib.p4thpymisc.src.misc import items
from contrib.p4thpymap.src.reducers.logical import all


def globalVersionGuard(_versionGuard=[]):
    if len(_versionGuard) < 1:
        _versionGuard.append(_VersionGuard)

    return _versionGuard[0]


class VersionGuardMismatchError(Exception):

    def __init__(self, msg, domainApproveMap, *args, **kwargs):
        super().__init__(self, msg, *args, **kwargs)
        self.domainApproveMap = domainApproveMap

    def __str__(self) -> str:
        res = super().__str__()
        pairs = '. '.join(['{}:{}'.format(key, val)
                          for key, val in items(self.domainApproveMap)])
        return '{} [{}]'.format(res, pairs)


class VersionGuardUnqiueVersionError(Exception):

    def __init__(self, msg, domain, versions, *args, **kwargs):
        super().__init__(self, msg, *args, **kwargs)
        self.domain = domain
        self.versions = versions

    def __str__(self) -> str:
        res = super().__str__()

        versions = ', '.join([d for d in items(self.versions)])
        return '{} [{} -> ({})]'.format(res, self.domain, versions)


class _VersionGuard():

    _domainVersionMap = {}
    approvedVersions = {}
    allowUnapprovedVersion = False
    log = logging.getLogger('VersionGuard')
    prototypes = []

    @classmethod
    def getDomainVersionMap(cls, *arg, ** kwargs):
        return cls._domainVersionMap

    @classmethod
    def setLog(cls, log: logging.Logger):
        cls.log = log

    @classmethod
    def setDomainVersion(cls, domain: str, version: str):

        _domainVersionMap = cls.getDomainVersionMap()
        if domain in _domainVersionMap:
            version0 = _domainVersionMap[domain]
            if version0 != version0:
                raise VersionGuardUnqiueVersionError(
                    'Multiple versions.', domain, [version0, version])
        else:
            _domainVersionMap[domain] = version

        cls.log.info('%s = v%s', domain, _domainVersionMap)

    @classmethod
    def setDomainVersionMap(cls, map: dict):
        for domain, version in items(map):
            cls.setDomainVersion(domain, version)

    @staticmethod
    def onNewClass(cls):
        if cls.allowUnapprovedVersion:
            return

        cls.verifyVersions()

    @classmethod
    def checkVersion(cls, version, approvedVersion) -> bool:
        if isinstance(approvedVersion, Iterable) and not isinstance(approvedVersion, str):
            return not R.find(lambda approvedVersion: not cls.checkVersion(version, approvedVersion))(approvedVersion)

        return match(version, approvedVersion)

    @classmethod
    def checkVersions(cls, domainVersionMap=None):

        _domainVersionMap = cls.getDomainVersionMap() \
            if domainVersionMap is None else domainVersionMap

        return {
            domain: cls.checkVersion(
                _domainVersionMap[domain], approvedVersion)
            if domain in _domainVersionMap else None
            for domain, approvedVersion in items(cls.approvedVersions)
        }

    @classmethod
    def areVersionsOk(cls, domainVersionMap=None):
        def isOk(val: bool | None, *args, **kwargs):
            return val is not False

        return all(cls.checkVersions(domainVersionMap), isOk)

    @classmethod
    def verifyVersions(cls):
        domainApprovedMap = cls.checkVersions()
        if R.find(lambda key: domainApprovedMap[key] is False)(domainApprovedMap):
            raise VersionGuardMismatchError(
                'Incompatible versions.', domainApprovedMap)
