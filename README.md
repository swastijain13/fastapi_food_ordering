# FastAPI Food Ordering System

A simple RESTful API for a food ordering system using FastAPI, SQLAlchemy, and MySQL.

## Features :-

- User signup/login with JWT authentication
- Admin can manage menu items
- Users can browse menu and place orders
- Admin can view all orders
- Users can view/cancel their orders

---

## Tech Stack:-

- Python 3.11+
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic
- JWT (Python-Jose)
- Pytest

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/swastijain13/fastapi_food_ordering.git
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3.Install Dependencies

```bash
pip install -r requirements.txt
```

### 4.Create Database

###### open mysql shell

```
create database your_database_name;
create database your_test_database_name;
```

### 5. update app.config.py file

```
DATABASE_URL = "your_database_name"
SECRET_KEY = "abc123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
TEST_DATABASE_URL = "your_test_db_name"
```

**Make sure your MySQL database exists.**

### 6. Run Server

```
uvicorn app.main:app --reload
```
