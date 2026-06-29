import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
from app.logging_config import setup_logging

logger = logging.getLogger(__name__)

setup_logging()
logger.info("logger initialized")

app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="app/frontend/static/"),
    name="static"
)

app.include_router(router)