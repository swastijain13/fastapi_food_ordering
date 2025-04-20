from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routes.auth import router as auth_router
from app.routes.admin import admin_router
from app.routes.user import user_router
from app.admin import create_admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

create_admin()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Food Ordering App"}
