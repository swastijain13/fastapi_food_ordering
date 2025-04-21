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
DATABASE_URL = "your_database_url" ("mysql+mysqlconnector://user:password@127.0.0.1:3306/your_db_name")
SECRET_KEY = "abc123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
TEST_DATABASE_URL = "your_test_db_url" ("mysql+mysqlconnector://user:password@127.0.0.1:3306/your_test_db_name")
```

**Make sure your MySQL database exists.**

### 6. Run Server

```
uvicorn app.main:app --reload
```

**The server will start on http://127.0.0.1:8000**

You can access the Swagger UI for all endpoints at:

http://127.0.0.1:8000/docs

### Project Structure

```
fastapi-foodordering/
│
├── app/
│   ├── main.py
│   ├── admin.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── config.py.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── admin.py
│   │   └── user.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_admin.py
│   ├── test_user.py
│   └── conftest.py
│
├── .gitignore
├── requirements.txt
└── README.md

```

## API Endpoints

### Auth

| Endpoint      | Method | Description              | Auth Required |
| ------------- | ------ | ------------------------ | ------------- |
| /auth/signup  | POST   | Register a new user      | No            |
| /auth/login   | POST   | Login and receive tokens | No            |
| /auth/logout  | POST   | Logout the user          | Yes           |
| /auth/me      | GET    | Get user details         | Yes           |
| /auth/me      | PUT    | Update user details      | Yes           |
| /auth/refresh | POST   | create new access token  | Yes           |

### Admin

| Endpoint         | Method | Description              | Auth Required |
| ---------------- | ------ | ------------------------ | ------------- |
| /admin/menu      | POST   | Add a new menu item      | Yes (Admin)   |
| /admin/menu/{id} | PUT    | Update a menu item by ID | Yes (Admin)   |
| /admin/menu/{id} | DELETE | Delete a menu item by ID | Yes (Admin)   |
| /admin/orders    | GET    | View all orders          | Yes (Admin)   |

### User

| Endpoint             | Method | Description             | Auth Required |
| -------------------- | ------ | ----------------------- | ------------- |
| /user/menu           | GET    | Browse menu             | No            |
| /user/order          | POST   | Place an order          | Yes           |
| /user/order/{id}     | DELETE | Cancel an order by ID   | Yes           |
| /user/orders/history | GET    | View user order history | Yes           |

## Running Tests

```
pytest
```
