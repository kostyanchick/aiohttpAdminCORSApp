from service_api.views import GuardView, AllowedOriginsView
from aiohttp import web


def load_api(app):
    api_v1 = web.Application()
    api_v1.router.add_view('/', GuardView)
    api_v1.router.add_view('/index', GuardView)

    admin = web.Application()
    admin.router.add_view('/allowed_origins', AllowedOriginsView)

    app.add_subapp('/api/v1', api_v1)
    app.add_subapp('/admin', admin)
