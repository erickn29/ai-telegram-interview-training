import json

import redis.asyncio as redis

from redis import RedisError

from core.config import config
from schema.user import UserModelSchema


class Cache:
    def __init__(
        self, host=config.redis.HOST, port=config.redis.PORT, db=config.redis.DB
    ):
        self.host = host
        self.port = port
        self.db = db
        self.connection_pool = redis.ConnectionPool(
            host=self.host, port=self.port, db=self.db
        )
        self.redis_cache = redis.StrictRedis(connection_pool=self.connection_pool)

    async def set(self, key: str, value: str, expire: int = 60):
        try:
            await self.redis_cache.set(key, value, expire)
        except RedisError:
            return

    async def get(self, key, decode="utf-8"):
        res = await self.redis_cache.get(key)
        if res:
            return res.decode(decode)
        return res

    async def delete(self, key: str):
        await self.redis_cache.delete(key)

    async def set_user(self, schema: UserModelSchema):
        schema.created_at = schema.created_at.strftime("%Y-%m-%d %H:%M:%S")
        schema.updated_at = schema.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        schema_string = json.dumps(schema.model_dump())
        await self.set(
            f"user:{str(schema.tg_id)}",
            schema_string,
            60 * 60 * 24 * 7,
        )

    async def get_user(self, key: str) -> UserModelSchema | None:
        res = await self.get(key)
        if res:
            schema = UserModelSchema.model_validate(json.loads(res))
            schema.id = int(schema.id)
            schema.tg_id = int(schema.tg_id)
            # schema.created_at = datetime.datetime.strptime(
            #     schema.created_at,
            #     "%Y-%m-%d %H:%M:%S",
            # )
            # schema.updated_at = datetime.datetime.strptime(
            #     schema.updated_at,
            #     "%Y-%m-%d %H:%M:%S",
            # )
            return UserModelSchema.model_validate(schema)
        return None


cache = Cache()
