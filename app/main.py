from fastapi import FastAPI, Request
from app.api.v1.chat_endpoints import router as chat_router
from app.core.logger import logger
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup logic
    logger.info("Starting up the FastAPI application")
    yield
    # Shutdown logic
    logger.info("Shutting down the FastAPI application")

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

# Include API routers
app.include_router(chat_router, prefix="/api/v1")

# Middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": "Welcome to the TA Assistant API! check the api swagger at localhost:8899/docs"}
