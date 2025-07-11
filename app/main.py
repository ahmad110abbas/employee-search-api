import logging
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from app.db.base import Base, engine
from app.api.employees import router as employees_router
from app.middlewares import rate_limit_middleware
import uvicorn

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Employee Search API",
    description="""
    A comprehensive API for searching and filtering employee data across organizations.
    
    ## Features
    * **Search by multiple criteria**: Filter employees by name, department, position, location, organization, and status
    * **Pagination support**: Efficiently handle large datasets with page-based pagination
    * **Caching**: Fast response times with intelligent caching
    * **Status filtering**: Filter by employee status (active, not_started, terminated)
    
    ## Rate Limiting
    API requests are rate-limited to ensure fair usage.
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "employees",
            "description": "Operations with employees. Search and filter employee data.",
        },
    ],
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Start request: {request.method} {request.url.path} - query_params={dict(request.query_params)}")
    response = await call_next(request)
    logger.info(f"End request: {request.method} {request.url.path} - status_code={response.status_code}")
    return response

app.middleware("http")(rate_limit_middleware)

app.include_router(employees_router, prefix="/api/v1", tags=["employees"])

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 