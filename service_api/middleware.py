from http import HTTPStatus
from functools import wraps

from service_api.app import db, app
from service_api.db.repositories import OriginRepository
from service_api.constants import HTTP_METHODS


def valid_origin_method(view_method):
    """This function applies to specific view methods"""

    @wraps(view_method)
    async def inner(cls, *args, **kwargs):
        req_origin = cls.request.headers.get('Origin')
        allowed_origins, status = await OriginRepository(db).get_all_origins()

        # check whether origin is allowed (is sub-domain)
        # if origin omitted, check whether host is the same as running server
        if req_origin:
            match = [origin for origin in allowed_origins if (origin in req_origin)]
        else:
            match = cls.request.headers['Host'].split(':')[0] == app.config['APP_HOST']

        if not match:
            message = {'error_message': 'Origin not allowed'}
            return cls._get_response(data=message, status=HTTPStatus.FORBIDDEN.value)
        else:
            return await view_method(cls, *args, **kwargs)

    return inner


def valid_origin_view(decorator=valid_origin_method):
    """This decorator apply decorator arg to all http methods in view class"""
    def decorate_class(cls):
        for method in HTTP_METHODS:
            try:
                # if view method exists - apply decorator
                method_name = method.lower()
                view_method = getattr(cls, method_name)
                print(f"Registering CORS middleware for {cls.__name__}.{view_method.__name__}")
                setattr(cls, method_name, decorator(view_method))
            except AttributeError:
                pass
        return cls
    return decorate_class
