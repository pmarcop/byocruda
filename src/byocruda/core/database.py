from typing import Generator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import StaticPool

from byocruda.core.config import settings
from byocruda.core.logging import log

# Custom MetaData instance with naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

class Base(DeclarativeBase):
    """Base class for all models"""
    metadata = metadata

# Create engine with connection pooling
engine = create_engine(
    settings.database.url,
    echo=settings.database.echo,
    connect_args={"check_same_thread": False},  # Only for SQLite
    poolclass=StaticPool  # Simplifies SQLite connections
)

# Create sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator:
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        log.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()

def init_db() -> None:
    """Initialize the database, creating all tables."""
    try:
        log.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        log.info("Database tables created successfully")
    except Exception as e:
        log.error(f"Error creating database tables: {str(e)}")
        raise
