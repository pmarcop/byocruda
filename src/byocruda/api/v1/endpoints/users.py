from fastapi import APIRouter, Request, Depends, HTTPException

from typing import List, Optional, Annotated, TYPE_CHECKING

from sqlmodel import Session, select

from byocruda.core.database import get_db_session

from byocruda.models.models import (
    UserBase, 
    User,
    UserPublic, 
    UserCreate, 
    UserPublicWithDepartment,
    UserUpdate
)


router = APIRouter()

@router.get("/", response_model=List[UserPublic])
async def get_users(
    *, 
    session: Session = Depends(get_db_session),
    limit: int = 100,
    skip: int = 0
    ):
    users=session.exec(select(User).offset(skip).limit(limit)).all()
    return users

@router.get("/{user_id}", response_model=UserPublicWithDepartment)
async def get_user(
    *,
    user_id: int,
    session : Session = Depends(get_db_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserPublic)
async def create_user(
    *,
    session: Session = Depends(get_db_session),
    user: UserCreate
):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
async def delete_user(
    *,
    session: Session = Depends(get_db_session),
    user_id: int
):
    user=session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"deleted": True}

@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(
    *,
    session: Session = Depends(get_db_session),
    user_id: int,
    user: UserUpdate
):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key,value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
