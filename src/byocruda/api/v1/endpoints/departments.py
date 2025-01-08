from typing import List

from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from byocruda.core.logging import log

from byocruda.models.models import (
    DepartmentPublic,
    Department, 
    DepartmentCreate, 
    DepartmentPublicWithUsers,
    DepartmentUpdate
    )
from byocruda.core.database import get_db_session


router = APIRouter()

@router.get("/", response_model=List[DepartmentPublic])
async def get_departments(
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    departments=session.exec(select(Department).offset(skip).limit(limit)).all()
    return departments

# @router.get("/{department_id}", response_model=DepartmentPublic)
# async def get_department(
#     *,
#     department_id: int,
#     session: Session = Depends(get_db_session)
    
# ):
#     department = session.get(Department, department_id)
#     if not department:
#         raise HTTPException(status_code=404, detail="Department not found")
#     return department

@router.get("/{department_id}", response_model=DepartmentPublicWithUsers)
async def get_department(
    *,
    department_id: int,
    session: Session = Depends(get_db_session)
    
):
    department = session.get(Department, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department



@router.post("/", response_model=DepartmentPublic)
async def create_department(*, session: Session = Depends(get_db_session), department: DepartmentCreate):
    db_department = Department.model_validate(department)
    session.add(db_department)
    session.commit()
    session.refresh(db_department)
    return db_department

@router.delete("/{department_id}")
async def delete_department(
    *,
    session : Session = Depends(get_db_session),
    department_id: int
):
    department = session.get(Department, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    session.delete(department)
    session.commit()
    return { "deleted": True }

@router.patch("/{department_id}", response_model=DepartmentPublic)
async def update_department(
    *,
    session: Session = Depends(get_db_session),
    department_id: int,
    department: DepartmentUpdate
):
    db_department = session.get(Department, department_id)
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    department_data = department.model_dump(exclude_unset=True)
    for key, value in department_data.items():
        setattr(db_department, key, value)
    session.add(db_department)
    session.commit()
    session.refresh(db_department)
    return db_department