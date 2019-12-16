import json
from http import HTTPStatus
from datetime import datetime

from aiohttp import web

from service_api.app import db
from service_api.utils import CustomJSONEncoder
from service_api.db.repositories import OriginRepository
from service_api.constants import HTTP_METHODS
from service_api.middleware import valid_origin_view


@valid_origin_view()
class BaseView(web.View):

    async def options(self, *args, **kwargs):
        allowed_methods = [method for method in HTTP_METHODS if hasattr(self, method.lower())]
        allowed_origins, status = await OriginRepository(db).get_all_origins()

        headers = {
            'Access-Control-Allow-Methods': ', '.join(allowed_methods),
            'Access-Control-Allow-Origin': ', '.join(allowed_origins)
        }

        return web.Response(text='', status=200, headers=headers)

    @staticmethod
    def _get_response(data, status, encoder=None):
        resp_obj = {
            'data': data,
            'status': 'success'
            if (status == HTTPStatus.OK.value or status == HTTPStatus.CREATED.value)
            else 'failed',
            'timestamp': str(datetime.utcnow())
        }
        dumped_obj = json.dumps(resp_obj, cls=encoder)

        return web.Response(body=dumped_obj, content_type='application/json', status=status)


@valid_origin_view()
class GuardView(BaseView):
    async def get(self):
        return web.json_response({'hello': 'world'})


@valid_origin_view()
class AllowedOriginsView(BaseView):
    async def get(self):
        """Get list of allowed origins"""
        result, status = await OriginRepository(db).get_many()

        resp_obj = result if (status == HTTPStatus.OK.value) else {'error_message': result}
        response = self._get_response(resp_obj, status, encoder=CustomJSONEncoder)

        return response

    async def post(self):
        """Add new origin to list of allowed"""
        origin_data = await self.request.json()
        result, status = await OriginRepository(db).create(data=origin_data)

        resp_obj = result if (status == HTTPStatus.CREATED.value) else {'error_message': result}
        response = self._get_response(resp_obj, status, encoder=CustomJSONEncoder)

        return response
