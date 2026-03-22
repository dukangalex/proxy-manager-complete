from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.api.app.schemas import UserCreate, UserUpdate
from apps.api.app.security import verify_admin_token
from apps.api.app.services import crud
from shared.db import get_db

router = APIRouter(prefix='/admin', tags=['admin'], dependencies=[Depends(verify_admin_token)])

@router.get('/users')
def list_users(db: Session = Depends(get_db)):
    return crud.list_users(db)

@router.post('/users')
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, payload.username, payload.days, payload.traffic_limit_gb)

@router.patch('/users/{username}')
def update_user(username: str, payload: UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db, username, enabled=payload.enabled, traffic_limit_gb=payload.traffic_limit_gb)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    return user

@router.delete('/users/{username}')
def delete_user(username: str, db: Session = Depends(get_db)):
    ok = crud.delete_user(db, username)
    if not ok:
        raise HTTPException(status_code=404, detail='user not found')
    return {'ok': True}

@router.post('/users/{username}/reset-sub')
def reset_sub(username: str, db: Session = Depends(get_db)):
    user = crud.reset_sub(db, username)
    if not user:
        raise HTTPException(status_code=404, detail='user not found')
    return user

@router.get('/nodes')
def list_nodes(db: Session = Depends(get_db)):
    return crud.list_nodes(db)
