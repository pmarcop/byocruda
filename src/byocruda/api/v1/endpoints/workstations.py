from fastapi import APIRouter, Request, Depends, HTTPException

from typing import List, Optional, Annotated, TYPE_CHECKING

from sqlmodel import Session, select

from byocruda.core.database import get_db_session

from byocruda.models.models import (
    Workstation,
    WorkstationBase,
    WorkstationCreate,
    WorkstationPublic,
    WorkstationUpdate,
    WorkstationType,
    WorkstationTypePublic,
    WorkstationTypeBase,
    WorkstationTypeCreate
)

router = APIRouter()

@router.get("/", response_model=List[WorkstationPublic])
async def get_workstations(
    *,
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    workstations = session.exec(select(Workstation).offset(skip).limit(limit)).all()
    return workstations

@router.get("/{workstation_id}", response_model=WorkstationPublic)
async def get_workstation(
    *,
    session: Session = Depends(get_db_session),
    workstation_id: int
):
    db_workstation = session.get(Workstation, workstation_id)
    if not db_workstation:
        raise HTTPException(status_code=404, detail="Workstation not found")
    return db_workstation

@router.post("/", response_model=WorkstationPublic)
async def create_workstation(
    *,
    session: Session = Depends(get_db_session),
    workstation: WorkstationCreate
):
    db_workstation = Workstation.model_validate(workstation)
    session.add(db_workstation)
    session.commit()
    session.refresh(db_workstation)
    return db_workstation

@router.delete("/{workstation_id}")
async def delete_workstation(
    *,
    workstation_id: int,
    session: Session = Depends(get_db_session)
):
    db_workstation=session.get(Workstation, workstation_id)
    if not db_workstation:
        raise HTTPException(status_code=404, detail="Workstation not found")
    session.delete(db_workstation)
    session.commit()
    return {"deleted": True}

@router.patch("/{workstation_id}", response_model=WorkstationPublic)
async def get_workstation(
    *,
    session: Session = Depends(get_db_session),
    workstation_id: int,
    workstation: WorkstationUpdate
):
    db_workstation = session.get(Workstation, workstation_id)
    if not db_workstation:
        raise HTTPException(status_code=404, detail="Workstation not found")
    workstation_data=workstation.model_dump(exclude_unset=True)
    for key, value in workstation_data:
        setattr(db_workstation, key, value)
    session.add(db_workstation)
    session.commit()
    session.refresh(db_workstation)
    return db_workstation

@router.get("/types", response_model=List[WorkstationTypePublic])
async def get_workstation_types(
    *,
    session : Session = Depends(get_db_session),
    offset: int = 0,
    limit: int = 100,
):
    workstation_types=session.exec(select(WorkstationType).offset(offset).limit(limit)).all()
    return workstation_types

@router.post("/types", response_model=WorkstationTypePublic)
async def create_workstation_type(
    *,
    session: Session = Depends(get_db_session),
    workstation_type: WorkstationTypeCreate
):
    db_workstation_type = WorkstationType.model_validate(workstation_type)
    session.add(db_workstation_type)
    session.commit()
    session.refresh(db_workstation_type)
    return db_workstation_type