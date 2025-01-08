from __future__ import annotations


from sqlalchemy import event
from sqlalchemy.pool import QueuePool
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlite3 import Connection as SQLite3Connection

from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

from byocruda.core.config import settings
from byocruda.core.logging import log

from byocruda.models import models

# Enable foreign key enforcement for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# Custom MetaData instance with naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = SQLModel.metadata
metadata.naming_convention = convention

def create_db_engine():
    """Create database engine with proper configuration."""
    connect_args = {"check_same_thread": False} if settings.database.url.startswith('sqlite') else {}
    
    return create_engine(
        settings.database.url,
        echo=settings.database.echo,
        connect_args=connect_args,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=3600        
    )

# Create engine with connection pooling
engine = create_db_engine()

# Create sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session # Use SQLModel Session class
)


def verify_database_connection() -> bool:
    """Verify database connection is working."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1")) # In SQLAlchemy 2.x SLQ statements must be parsed with text() function
        log.info("Database connection verified successfully")
        return True
    except Exception as e:
        log.error(f"Database connection verification failed: {str(e)}")
        return False
    return True

def get_db_session() -> Generator[Session, None, None]:
    """Database session dependency."""
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        log.error(f"Database session error: {str(e)}")
        raise
    finally:
        session.close()

def init_db() -> None:
    """Initialize the database, creating all tables."""
    try:
        log.info("Verifying database connection...")
        if not verify_database_connection():
            raise Exception("Database connection verification failed")
            
        log.info("Creating database tables...")
        SQLModel.metadata.create_all(bind=engine)
        log.info("Database tables created successfully")
    except Exception as e:
        log.error(f"Error initializing database: {str(e)}")
        raise

def cleanup_db() -> None:
    """Cleanup database connections."""
    try:
        engine.dispose()
        log.info("Database connections cleaned up successfully")
    except Exception as e:
        log.error(f"Error cleaning up database connections: {str(e)}")
        raise
