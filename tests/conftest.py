import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import timedelta
from app.routes.auth import create_access_token, get_password_hash
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.database import get_db, TestingSessionLocal, Base
from app.models import *
from app.main import app

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@pytest.fixture(autouse=True)
def setup_test_db():
    engine = TestingSessionLocal.kw["bind"]
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db: Session):
    app.dependency_overrides[get_db] = lambda: db
    return TestClient(app)

def authenticate_admin_client(db):
    admin_user = User(username="admin", email="admin@example.com", password_hash = get_password_hash("adminpass"), role="admin")

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    access_token = create_access_token(data={"sub":str(admin_user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    app.dependency_overrides[get_db] = lambda:db

    client = TestClient(app)
    client.headers.update({"Authorization" : f"Bearer {access_token}"})
    return client


def authenticate_user_client(db):
    user = User(username="TestUser", email="TestUser@example.com", password_hash=get_password_hash("TestPasssword"), role="user")

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub" : str(user.id)}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    app.dependency_overrides[get_db] = lambda: db

    client = TestClient(app)
    client.headers.update({"Authorization" : f"Bearer {token}"})
    return client


@pytest.fixture
def authenticated_admin_client(db):
    return authenticate_admin_client(db)

@pytest.fixture
def authenticated_user_client(db):
    return authenticate_user_client(db)



