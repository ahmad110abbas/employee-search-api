from fastapi import FastAPI
from .app.database import engine, Base
from .app.models import Employee
from .app.routes import router
from .app.middlewares import rate_limit_middleware
import uvicorn

app = FastAPI()

# Include middleware
app.middleware("http")(rate_limit_middleware)

# Include routes
app.include_router(router)

# Create database tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)