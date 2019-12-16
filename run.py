from aiohttp import web

from service_api.app import app
from service_api.api import load_api

if __name__ == '__main__':
    load_api(app)

    web.run_app(app,
                host=app.config['APP_HOST'],
                port=app.config['APP_PORT'],
                access_log_format=app.config['ACCESS_LOG_FORMAT'])
