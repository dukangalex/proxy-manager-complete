import json
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from shared import models
from shared.config import get_settings


def create_user(db: Session, username: str, days: int, traffic_limit_gb: int):
    user = models.User(
        username=username,
        uuid=str(uuid4()),
        sub_token=str(uuid4()) + str(uuid4()),
        expire_at=datetime.utcnow() + timedelta(days=days),
        traffic_limit_gb=traffic_limit_gb,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session):
    return db.scalars(select(models.User).order_by(models.User.created_at.desc())).all()


def get_user(db: Session, username: str):
    return db.scalar(select(models.User).where(models.User.username == username))


def get_user_by_token(db: Session, token: str):
    return db.scalar(select(models.User).where(models.User.sub_token == token))


def update_user(db: Session, username: str, enabled=None, traffic_limit_gb=None):
    user = get_user(db, username)
    if not user:
        return None
    if enabled is not None:
        user.enabled = enabled
    if traffic_limit_gb is not None:
        user.traffic_limit_gb = traffic_limit_gb
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, username: str):
    user = get_user(db, username)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def reset_sub(db: Session, username: str):
    user = get_user(db, username)
    if not user:
        return None
    user.sub_token = str(uuid4()) + str(uuid4())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def ensure_default_nodes(db: Session):
    if db.scalars(select(models.Node)).first():
        return
    s = get_settings()
    nodes = [
        models.Node(name='Reality-Primary', type='reality', server=s.server_address, port=s.reality_port, enabled=True, meta_json=json.dumps({'sni': s.reality_sni, 'public_key': s.reality_public_key, 'short_id': s.reality_short_id})),
        models.Node(name='HY2-Primary', type='hy2', server=s.server_address, port=s.hy2_port, enabled=True, meta_json=json.dumps({'sni': s.hy2_sni, 'insecure': s.hy2_insecure})),
    ]
    db.add_all(nodes)
    db.commit()


def list_nodes(db: Session):
    return db.scalars(select(models.Node).order_by(models.Node.id.asc())).all()
