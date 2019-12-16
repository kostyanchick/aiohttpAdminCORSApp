from service_api.constants import ALLOWED_ORIGINS_COLLECTION
from service_api.db import BaseRepository


class OriginRepository(BaseRepository):
    collection_name = ALLOWED_ORIGINS_COLLECTION

    async def get_all_origins(self):
        return await self.get_many(
            projection={'origin': 1},
            distinct_by=['origin']
        )

