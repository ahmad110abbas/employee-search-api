import time
from fastapi import Request
from fastapi.responses import JSONResponse
from .config import get_config
from .cache import redis_client

config = get_config()
RATE_LIMIT = config.getint('RATE_LIMIT', 'REQUESTS_PER_MINUTE')
RATE_LIMIT_WINDOW = config.getint('RATE_LIMIT', 'WINDOW_SECONDS')

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    current_minute = int(time.time() // 60)
    rate_key = f"rate_limit:{client_ip}:{current_minute}"
    
    current_count = redis_client.get(rate_key)
    if current_count is None:
        redis_client.setex(rate_key, RATE_LIMIT_WINDOW, 1)
        current_count = 1
    else:
        current_count = int(current_count) + 1
        redis_client.incr(rate_key)
    
    if current_count > RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={
                "detail": f"Rate limit exceeded: {RATE_LIMIT} requests per minute"
            },
            headers={"Retry-After": str(RATE_LIMIT_WINDOW)}
        )
    
    response = await call_next(request)
    return response