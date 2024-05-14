"""Functionality relating to database connections."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from v1.settings import DEBUG_DATABASE, db_info

db_engine = create_engine(url=db_info.url, echo=DEBUG_DATABASE)
DbSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


def get_db_session() -> Generator[Session, None, None]:
    """Yield database session."""
    db_session = DbSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
