import psycopg2
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

env_file_path = ".env.dev"

load_dotenv(dotenv_path=env_file_path)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

