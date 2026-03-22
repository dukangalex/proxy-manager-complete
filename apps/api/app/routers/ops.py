from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.app.security import verify_admin_token
from apps.api.app.services import crud
from apps.api.app.services.alert_center import create_alert
from apps.api.app.services.diagnostics import explain_error
from apps.api.app.services.node_health import check_node
from shared.db import get_db

router = APIRouter(prefix='/ops', tags=['ops'], dependencies=[Depends(verify_admin_token)])

@router.get('/health')
def health(db: Session = Depends(get_db)):
    nodes = [check_node(n) for n in crud.list_nodes(db)]
    failed = [n for n in nodes if not n['check']['ok']]
    if failed:
        create_alert(db, 'WARN', 'NODE_UNHEALTHY', '节点异常', failed[0]['check']['detail'], explain_error('NODE_UNHEALTHY'))
    return {'ok': len(failed) == 0, 'nodes': nodes}

@router.get('/status')
def status(db: Session = Depends(get_db)):
    return {'users': len(crud.list_users(db)), 'nodes': [check_node(n) for n in crud.list_nodes(db)]}
