from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MenuItem, Order, User
from app.schemas import MenuItemResponse, OrderCreate, OrderResponse
from app.routes.auth import get_current_user

user_router = APIRouter(tags=["User"])

@user_router.get("/menu", response_model=List[MenuItemResponse])
def browse_menu(db: Session = Depends(get_db)):
    menu = db.query(MenuItem).all()
    return menu


@user_router.post("/order", response_model=OrderResponse)
def place_order(order_data: OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_order = Order(user_id=user.id, menu_id=order_data.menu_id, quantity=order_data.quantity)
    db.add(new_order)
    db.commit()
    return new_order


@user_router.delete("/order/{id}")
def cancel_order(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == id, Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order cancelled"}


@user_router.get("/orders/history", response_model=List[OrderResponse])
def order_history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    return orders
