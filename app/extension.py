from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_BASE_DIR, DB_DIALECT, DB_NAME


def init_engine():
    """Create sqlalchemy engine"""

    URI: str = f"{DB_DIALECT}:///{DB_BASE_DIR}/{DB_NAME}"
    return create_engine(URI, echo=False)


def init_session():
    """Create sqlalchemy session"""

    return sessionmaker()
