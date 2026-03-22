from fastapi import Header, HTTPException, status
from shared.config import get_settings


def verify_admin_token(x_admin_token: str | None = Header(default=None)) -> str:
    token = get_settings().app_admin_token
    if not x_admin_token or x_admin_token != token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid admin token')
    return x_admin_token
