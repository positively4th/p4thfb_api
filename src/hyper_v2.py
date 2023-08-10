import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve

from api_v2 import app
from api_v2 import configGetter

config = Config()
config.bind = '127.0.0.1:3000'
config.keep_alive_timeout = 60*60

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    if configGetter('DEBUG'):
        loop.set_debug = True
    loop.run_until_complete(serve(app, config))
