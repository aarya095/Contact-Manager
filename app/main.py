import logging

from fastapi import FastAPI
from app.routes import router
from app.logging_config import setup_logging

logger = logging.getLogger(__name__)

setup_logging()
logger.info("logger initialized")
app = FastAPI()
app.include_router(router)