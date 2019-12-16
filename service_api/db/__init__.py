from http import HTTPStatus


class BaseRepository:
    collection_name = NotImplemented

    def __init__(self, db):
        self.db = db
        self.collection = db[self.collection_name]

    async def _get(self, query: dict, projection: dict, limit: int, distinct_by: list):
        try:
            # get by id
            if isinstance(query, str):
                result = await self.collection.find_one({'_id': query}, projection)
            # get by query list of elements
            else:
                cursor = self.collection.find(query, projection)
                if limit:
                    cursor = cursor.limit(limit)
                if distinct_by:
                    result = await cursor.distinct(*distinct_by)
                else:
                    result = [rec async for rec in cursor]
            status = HTTPStatus.OK.value
            return result, status
        # connection error
        except Exception as ex:
            print(ex)
            status = HTTPStatus.SERVICE_UNAVAILABLE.value
            return str(ex), status

    async def get_by_id(self, doc_id, projection=None):
        return await self._get(query=doc_id, projection=projection)

    async def get_many(self, query=None, projection=None, limit=None, distinct_by=None):
        return await self._get(query=query, projection=projection,
                               limit=limit, distinct_by=distinct_by)

    async def create(self, data):
        try:
            if isinstance(data, list):
                await self.collection.insert_many(data)
            else:
                await self.collection.insert_one(data)
            status = HTTPStatus.CREATED.value
            return data, status
        except Exception as ex:
            print(ex)
            status = HTTPStatus.SERVICE_UNAVAILABLE.value
            return str(ex), status

    async def create_many(self, data):
        return await self.create(data)
