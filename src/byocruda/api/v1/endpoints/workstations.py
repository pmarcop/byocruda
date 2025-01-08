from fastapi import APIRouter, Request, Depends, HTTPException

from typing import List, Optional, Annotated, TYPE_CHECKING

from sqlmodel import Session, select

from byocruda.core.database import get_db_session

from byocruda.models.models import (
    Workstation,
    WorkstationBase,
    WorkstationCreate,
    WorkstationPublic,
    WorkstationType,
    WorkstationUpdate
)

router = APIRouter()

@router.get("/workstations", response_model=List[WorkstationPublic])
async def get_workstations(
    *,
    session: Session = Depends(get_db_session),
    skip: int = 0,
    limit: int = 100
):
    workstations = session.exec(select(Workstation).offset(skip).limit(limit)).all()
    return workstations

# @router.post("/workstations", response_model=WorkstationPublic)
# async def create_workstation(
#     *,
#     session: Session = Depends(get_db_session),
#     workstation: WorkstationCreate
# ):
#     db_workstation = Workstation.model_validate(workstation)
#     session.add(db_workstation)
#     session.commit()
#     session.refresh(db_workstation)
#     return workstation