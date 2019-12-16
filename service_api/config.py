import os


class Config:
    APP_HOST = os.getenv('HOST', 'localhost')
    APP_PORT = int(os.getenv('PORT', 8080))

    MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
    MONGO_PORT = os.getenv('MONGO_PORT', 27117)
    MONGO_DB_NAME = 'cors_db'

    ACCESS_LOG_FORMAT = " :: %r %s %T %t"

    def __getitem__(self, item):
        return self.__getattribute__(item)
