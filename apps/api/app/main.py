from fastapi import FastAPI
from routers import admin

app = FastAPI()
app.include_router(admin.router)

@app.get("/health")
def health():
    return {"ok": True}
