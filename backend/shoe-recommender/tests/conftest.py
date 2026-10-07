import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from shoe_recommender.database.models import Base


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
    )

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
    
    Base.metadata.create_all(engine)
    
    with session_factory() as session:
        yield session

    # engine.dispose()