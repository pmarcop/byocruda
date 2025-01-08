from typing import List, Optional
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, LargeBinary, Text, text
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint

from byocruda.models.users import *
from byocruda.models.departments import *
from byocruda.models.workstations import *

class DepartmentPublicWithUsers(DepartmentPublic):
    users: List["UserPublic"] | None = []

class UserPublicWithDepartment(UserPublic):
    department: Optional["DepartmentPublic"] | None = None

    
# class WorkstationType(SQLModel, table=True):
#     __tablename__ = 'workstation_types'

#     workstation_type_id: int = Field(primary_key=True, unique=True, nullable=False)
#     type: str = Field(nullable=False, unique=True)

#     workstations: List['Workstation'] = Relationship(back_populates='workstation_types', passive_deletes="all")


# class Workstation(SQLModel, table=True):
#     __tablename__ = 'workstation'
#     workstation_id: int = Field(primary_key=True, unique=True, nullable=False)
#     hostname: str = Field(nullable=False, unique=True)
#     type_id: int = Field(foreign_key='workstation_types.workstation_type_id', ondelete='RESTRICT', nullable=False, default=1)
#     user_id: int = Field(foreign_key='users.user_id', ondelete='SET DEFAULT', nullable=False, default=1)
#     date_of_arrival: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc))

#     workstation_types: Optional['WorkstationType'] = Relationship(back_populates='workstations')
#     user: Optional['Users'] = Relationship(back_populates='workstations')

# class OtherAssets(SQLModel, table=True):
#     __tablename__= 'other_assets'
#     other_asset_id: int = Field(primary_key=True, unique=True, nullable=False)
#     name: str | None
#     department_id: int = Field(foreign_key='departments.department_id', ondelete='RESTRICT, ')
