from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_USERNAME =  "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_EMAIL =  "admin@gmail.com"

def create_admin():
    db: Session = SessionLocal()
    admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()
    
    if not admin:
        hashed_password = pwd_context.hash(ADMIN_PASSWORD)
        admin_user = User(username=ADMIN_USERNAME, email=ADMIN_EMAIL,password_hash=hashed_password, role="admin")
        db.add(admin_user)
        db.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists.")

    db.close()
