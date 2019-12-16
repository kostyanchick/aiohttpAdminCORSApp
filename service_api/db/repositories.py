from service_api.constants import ALLOWED_ORIGINS_COLLECTION
from service_api.db import BaseRepository


class OriginRepository(BaseRepository):
    collection_name = ALLOWED_ORIGINS_COLLECTION

