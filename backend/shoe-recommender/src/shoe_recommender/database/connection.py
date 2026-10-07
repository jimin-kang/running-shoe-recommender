from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from shoe_recommender.database.models import Base
from shoe_recommender.config import settings

# Establish DB connection
settings.database_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)
engine = create_engine(
    f"sqlite:///{settings.database_path}",
    connect_args={"check_same_thread": False}, # TODO: what is this?
)

# Create sessionmaker to handle transactions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def create_database() -> None:
    """
    Create DB tables.
    """
    Base.metadata.create_all(bind=engine)
    
def get_db() -> Generator[Session, None, None]:
    """
    Yields a database session
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()