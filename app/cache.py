import redis
import json
import hashlib
from .config import get_config

config = get_config()
REDIS_EXPIRE_SECONDS = config.getint('REDIS', 'EXPIRE_SECONDS')

redis_client = redis.Redis(
    host=config.get('REDIS', 'HOST'),
    port=config.getint('REDIS', 'PORT'),
    db=config.getint('REDIS', 'DB'),
    decode_responses=True
)

def generate_cache_key(filters: dict, page: int, size: int) -> str:
    key_data = {
        "filters": filters,
        "page": page,
        "size": size
    }
    return f"emp_search:{hashlib.sha256(json.dumps(key_data, sort_keys=True).encode()).hexdigest()}"

def get_cached_data(key: str):
    return redis_client.get(key)

def set_cached_data(key: str, data: dict):
    redis_client.setex(key, REDIS_EXPIRE_SECONDS, json.dumps(data))