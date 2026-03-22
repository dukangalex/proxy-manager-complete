from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.app.security import verify_admin_token
from apps.api.app.services.alert_center import create_alert, list_alerts
from apps.api.app.services.diagnostics import explain_error
from shared.db import get_db

router = APIRouter(prefix='/alerts', tags=['alerts'], dependencies=[Depends(verify_admin_token)])

@router.get('')
def alerts(db: Session = Depends(get_db)):
    return list_alerts(db)

@router.post('/test')
def test_alert(db: Session = Depends(get_db)):
    return create_alert(db, 'WARN', 'TEST_ALERT', '测试告警', '这是一条测试告警', ['忽略即可', '检查 TG 推送是否正常'])

@router.get('/diagnostics/{code}')
def diagnostics(code: str):
    return {'code': code, 'solutions': explain_error(code)}
