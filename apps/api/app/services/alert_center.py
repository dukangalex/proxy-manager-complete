import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from shared import models


def create_alert(db: Session, level: str, code: str, title: str, detail: str, solutions: list[str]):
    alert = models.Alert(level=level, code=code, title=title, detail=detail, solutions=json.dumps(solutions, ensure_ascii=False))
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def list_alerts(db: Session, limit: int = 20):
    return db.scalars(select(models.Alert).order_by(models.Alert.created_at.desc()).limit(limit)).all()
