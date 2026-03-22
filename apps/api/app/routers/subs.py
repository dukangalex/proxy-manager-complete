from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from apps.api.app.services import crud, subscription
from shared.db import get_db

router = APIRouter(tags=['subs'])

@router.get('/sub/{token}')
def sub_b64(token: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=404, detail='token not found')
    return Response(content=subscription.b64_links(user), media_type='text/plain; charset=utf-8')

@router.get('/sub-raw/{token}')
def sub_raw(token: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=404, detail='token not found')
    return Response(content=subscription.raw_links(user), media_type='text/plain; charset=utf-8')

@router.get('/clash/{token}')
def clash(token: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=404, detail='token not found')
    return Response(content=subscription.clash_profile(user), media_type='text/yaml; charset=utf-8')
