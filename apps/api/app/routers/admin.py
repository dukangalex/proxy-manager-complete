from fastapi import APIRouter

router = APIRouter(prefix="/admin")

users = []

@router.get("/users")
def list_users():
    return users

@router.post("/users")
def create_user(u: dict):
    users.append(u)
    return u
