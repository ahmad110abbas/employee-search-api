import logging
from fastapi import FastAPI, Request
from .app.database import engine, Base
from .app.models import Employee
from .app.routes import router
from .app.middlewares import rate_limit_middleware
import uvicorn

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Start request: {request.method} {request.url.path} - query_params={dict(request.query_params)}")
    response = await call_next(request)
    logger.info(f"End request: {request.method} {request.url.path} - status_code={response.status_code}")
    return response

# Include middleware
app.middleware("http")(rate_limit_middleware)

# Include routes
app.include_router(router)

# Create database tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)