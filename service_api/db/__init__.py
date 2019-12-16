from http import HTTPStatus


class BaseRepository:
    collection_name = NotImplemented

    def __init__(self, db):
        self.db = db
        self.collection = db[self.collection_name]

    async def _get(self, query, limit=None):
        try:
            # get by id
            if isinstance(query, str):
                result = await self.collection.find_one({'_id': query})
            # get by query list of elements
            else:
                cursor = self.collection.find(query)
                if limit:
                    cursor = cursor.limit(limit)
                result = [rec async for rec in cursor]
            status = HTTPStatus.OK.value
            return result, status
        # connection error
        except Exception as ex:
            print(ex)
            status = HTTPStatus.SERVICE_UNAVAILABLE.value
            return str(ex), status

    async def get_by_id(self, doc_id):
        return await self._get(query=doc_id)

    async def get_many(self, query=None, limit=None):
        return await self._get(query=query, limit=limit)

    async def insert(self, data):
        try:
            if isinstance(data, list):
                await self.collection.insert_many(data)
            else:
                await self.collection.insert(data)
            status = HTTPStatus.CREATED.value
            return data, status
        except Exception as ex:
            print(ex)
            status = HTTPStatus.SERVICE_UNAVAILABLE.value
            return str(ex), status

    async def insert_many(self, data):
        return await self.insert(data)