import os
import json
import redis


class CacheManager:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.password = os.getenv("REDIS_PASSWORD")

        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=True,
        )

    def exists(self, key: str) -> bool:
        return self.client.exists(key) == 1

    def get(self, key: str):
        value = self.client.get(key)
        if value is None:
            return None
        return json.loads(value)

    def set(self, key: str, value, ttl: int = 60):
        self.client.setex(
            name=key,
            time=ttl,
            value=json.dumps(value),
        )
