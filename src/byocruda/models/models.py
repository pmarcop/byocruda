from typing import List, Optional, Annotated
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

class UserPublicWithEverything(UserPublicWithDepartment):
    workstations: List["WorkstationPublic"] | None = None

class WorkstationPublicWithUserAndDepartment(WorkstationPublic):
    user: Optional["UserPublic"] | None = None
    department: Optional["DepartmentPublic"] | None = None