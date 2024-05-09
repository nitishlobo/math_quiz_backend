"""Global project settings."""

import os
from pathlib import Path

from dotenv import load_dotenv

from v1.schemas.database import DatabaseInfo
from v1.utils.utils import convert_string_to_bool

ENV_FILEPATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_FILEPATH)

# Database settings
DEBUG_DATABASE = convert_string_to_bool(os.getenv("DEBUG_DATABASE", default="False"))
DEBUG_TEST_DATABASE = convert_string_to_bool(os.getenv("DEBUG_TEST_DATABASE", default="True"))

db_info = DatabaseInfo(
    type_=os.getenv("DATABASE_TYPE", default="postgresql"),
    user=os.getenv("DATABASE_USER", default="admin"),
    password=os.getenv("DATABASE_PASSWORD", default="DummyPassword"),
    host=os.getenv("DATABASE_HOST", default="localhost"),
    port=int(os.getenv("DATABASE_PORT", default="5432")),
    name=os.getenv("DATABASE_NAME", default="quiz"),
)

# FastAPI application settings
APP_TITLE = os.getenv("APP_TITLE", default="Math Quiz")
# DEBUG_FASTAPI_APP provides debug traceback on server errors.
DEBUG_FASTAPI_APP = convert_string_to_bool(os.getenv("DEBUG_FASTAPI_APP", default="True"))
