import pytest
from sqlalchemy.orm import Session
from byocruda.core.database import get_db, init_db
from byocruda.models.models import User

@pytest.fixture(scope="function")
def db():
    """Database test fixture."""
    # Initialize database
    init_db()
    
    # Get database session
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

def test_create_user(db: Session):
    """Test user creation in database."""
    user = User(
        username="testuser",
        email="test@example.com",
        full_name="Test User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True

def test_user_timestamp_mixin(db: Session):
    """Test timestamp mixin functionality."""
    user = User(
        username="timeuser",
        email="time@example.com"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.created_at is not None
    assert user.updated_at is not None
