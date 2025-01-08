from typing import List, Optional
from typing_extensions import Annotated
from pydantic import StringConstraints, field_validator
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, LargeBinary, Text, text
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint

from byocruda.models.workstations import *

class UserBase(SQLModel):
    __table_args__ = (
        CheckConstraint('"Status" <= 2 AND "Status" >= 0'),
    )
    __tablename__ = 'users'
    userDN: str = Field(unique=True, index=True, schema_extra={'examples': ['a123z']})
    name: str = Field(nullable=False)
    department_id: int = Field(foreign_key='departments.department_id', ondelete='RESTRICT')
    notes: Optional[str] = Field(default=None)
    status: Optional[int] = Field(default=1)
    office_location: Optional[str] = Field(default=None)
    date_of_arrival: Optional[str] = Field(default_factory=lambda: f"{datetime.now().date()}")
    date_of_leave: Optional[str] = Field(default=None)
    # picture: Optional[bytes] = Field(default=None, sa_column=Column('picture', LargeBinary))

class User(UserBase, table=True):
    user_id: int | None = Field(primary_key=True, default= None)
    department: Optional['Department'] = Relationship(back_populates='users')
    workstations: List['Workstation'] = Relationship(back_populates='user', passive_deletes="all")

class UserPublic(UserBase):
    user_id: int

class UserCreate(UserBase):
    pass

class UserUpdate(SQLModel):
    name: str | None = Field(None, schema_extra={"examples": ["FullName"]})
    department_id: int | None = None
    notes: str | None = None
    status: int | None = None
    office_location: str | None = None
    date_of_leave: Annotated[str | None, StringConstraints(strip_whitespace=True)] = None

    @field_validator('date_of_leave')
    @classmethod
    def validate_date_of_leave(cls, value: str) -> str:
        date_format='%Y-%m-%d'
        try: 
            datetime.strptime(value, date_format)
            return value
        except ValueError:
            raise
