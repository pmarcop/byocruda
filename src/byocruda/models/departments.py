from typing import List, Optional
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, LargeBinary, Text, text
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, timezone
from sqlalchemy import UniqueConstraint

from byocruda.models.users import UserBase, User, UserPublic
from byocruda.models.workstations import WorkstationBase, Workstation, WorkstationPublic

class DepartmentBase(SQLModel):
    __tablename__ = 'departments'
    name: str = Field(unique=True, index=True)

class Department(DepartmentBase, table=True):
    department_id: int | None = Field(primary_key=True, default=None)
    users: List['User'] = Relationship(back_populates='department', passive_deletes="all")
    workstations: List['Workstation'] = Relationship(back_populates='department', passive_deletes="all")

class DepartmentPublic(DepartmentBase):
    department_id: int 

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(SQLModel):
    name: str | None = None
