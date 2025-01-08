from typing import List, Optional
from typing_extensions import Annotated
from pydantic import StringConstraints, field_validator
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, LargeBinary, Text, text
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint

class WorkstationType(SQLModel, table=True):
    __tablename__ = 'workstation_types'

    workstation_type_id: int = Field(primary_key=True)
    type: str = Field(unique=True)

    workstations: List['Workstation'] = Relationship(back_populates='workstation_type', passive_deletes="all")


# class WorkstationBase(SQLModel):
#     hostname: str = Field(nullable=False, unique=True)
#     type_id: int = Field(foreign_key='workstation_types.workstation_type_id', ondelete='RESTRICT')
#     user_id: int = Field(foreign_key='users.user_id', ondelete='RESTRICT')
#     department_id: int = Field(foreign_key='departments.department_id', ondelete='RESTRICT')
#     date_of_arrival: Optional[str] = Field(default_factory=lambda: f"{datetime.now().date()}")
#     video_ram_gb: int | None = None
#     system_ram_gb: int | None = None
#     total_storage_tb: int | None = None
#     hardware_description: Optional[str] = None
#     reserved: str | None = None
#     notes: str | None = None

class WorkstationBase(SQLModel):
    __tablename__ = 'workstation'
    hostname: str = Field(unique=True)
    type_id: int = Field(foreign_key='workstation_types.workstation_type_id', ondelete='RESTRICT')
    user_id: int = Field(foreign_key='users.user_id', ondelete='RESTRICT')
    department_id: int = Field(foreign_key='departments.department_id', ondelete='RESTRICT')
    # date_of_arrival: Optional[str] = Field(default_factory=lambda: f"{datetime.now().date()}")
    # video_ram_gb: int | None = None
    # system_ram_gb: int | None = None
    # total_storage_tb: int | None = None
    # hardware_description: Optional[str] = None
    # reserved: str | None = None
    # notes: str | None = None

    
class Workstation(WorkstationBase, table=True):
    workstation_id: int | None = Field(primary_key=True, default= None)
    workstation_type: Optional['WorkstationType'] = Relationship(back_populates="workstations")
    user: Optional['User'] = Relationship(back_populates="workstations")
    department: Optional['Department'] = Relationship(back_populates="workstations")

class WorkstationPublic(WorkstationBase):
    workstation_id: int

class WorkstationCreate(WorkstationBase):
    pass

class WorkstationUpdate(SQLModel):
    type_id: int | None = None
    user_id: int | None = None
    department_id: int | None = None
    # video_ram_gb: int | None = None
    # system_ram_gb: int | None = None
    # total_storage_tb: int | None = None
    # hardware_description: Optional[str] = None
    # reserved: str | None = None
    # notes: str | None = None
