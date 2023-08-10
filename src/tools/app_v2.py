from logging import getLogger
from functools import wraps
import asyncio
from datetime import datetime

from src.tools.app import App as App0
from src.mixins.contextlogger import ContextLogger


class App(App0):

    @classmethod
    def addRoute(cls, app, prefix: str, path: str, handler: dict, logger: None, timelogDB=None):

        _logger = getLogger() if logger is None else logger

        def createloggedRoute(fullPath: str, f: callable, args: tuple | list, kwArgs: dict):

            parts = fullPath.split('=')
            queryString = parts[1] if len(parts) > 1 else ''

            @wraps(f)
            async def wrappedHandler(*args, **kwargs):
                try:
                    res = ContextLogger.asLogged(f, tag=fullPath, staticData={
                        'traceId': datetime.now().isoformat(),
                        'queryString': queryString,
                    })(*args, **kwargs)
                    if asyncio.iscoroutine(res):
                        res = await res
                    return res
                except asyncio.CancelledError as e:
                    _logger.error('CancelledError: %s: %s',
                                  fullPath, f.__name__)
                    raise e

            return wrappedHandler

        def joinIf(parts, sep):
            return sep.join([
                part for part in parts if part != ''
            ])

        fullPath = joinIf([
            prefix.rstrip('/'),
            path.strip('/'),
        ], '/')
        f = handler[0]
        args = handler[1]
        kwArgs = {**{'strict_slashes': False}, **handler[2]}
        app.route(fullPath, *args, **kwArgs)(
            f if timelogDB is None else createloggedRoute(
                fullPath, f, args, kwArgs)
        )
        _logger.info('Added route %s.', fullPath)
