from typing import AsyncGenerator
from config import settings
import redis.asyncio as redis
from contextlib import asynccontextmanager


class RedisService:
    def __init__(self):
        host = settings.redis.redis_host
        port = settings.redis.redis_port
        self.__url = f'redis://{host}:{port}'
        self.__encoding = 'utf8'
        self.__decode_responses = True

    @asynccontextmanager
    async def client(self) -> AsyncGenerator[redis.Redis, None]:
        '''
        Клиент Redis-сервиса

        Yields:
            Iterator[AsyncGenerator[redis.Redis, None]]: Клиент \
                Redis-сервиса, подключающийся к сервису после каждого \
                    его вызова
        '''
        pool = redis.ConnectionPool.from_url(
            self.__url,
            encoding=self.__encoding,
            decode_responses=self.__decode_responses
        )

        _client = redis.Redis.from_pool(pool)
        try:
            yield _client
        finally:
            await _client.aclose()
