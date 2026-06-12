import os
from dotenv import load_dotenv

env_file_path = ".env.dev"
load_dotenv(dotenv_path = env_file_path)

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    MASTER_KEY = os.getenv("MASTER_KEY")

config = Config()