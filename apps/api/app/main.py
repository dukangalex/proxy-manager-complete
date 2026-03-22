from fastapi import FastAPI
from apps.api.app.routers import admin, subs, ops, alerts
from apps.api.app.services.crud import ensure_default_nodes
from shared.db import Base, SessionLocal, engine

app = FastAPI(title='Proxy Manager Complete')
app.include_router(admin.router)
app.include_router(subs.router)
app.include_router(ops.router)
app.include_router(alerts.router)

@app.on_event('startup')
def startup():
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        ensure_default_nodes(db)

@app.get('/health')
def health():
    return {'ok': True}
