import os
from dotenv import load_dotenv

env_file_path = ".env.test"
load_dotenv(dotenv_path = env_file_path)

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    MASTER_KEY = os.getenv("MASTER_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_TIME = os.getenv("ACCESS_TOKEN_EXPIRE_TIME")

config = Config()