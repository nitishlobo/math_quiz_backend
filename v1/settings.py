"""Global project settings."""
import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILEPATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_FILEPATH)

# Database settings
DEBUG_DATABASE = False
DATABASE_TYPE = os.getenv("DATABASE_TYPE")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_URL = f"{DATABASE_TYPE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
