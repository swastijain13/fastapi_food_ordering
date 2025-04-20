from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MenuItem, Order, User
from app.schemas import MenuItemCreate, MenuItemResponse, OrderResponse
from app.routes.auth import get_current_user

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

def is_admin(user: User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")


@admin_router.post("/menu")
def add_menu_item(menu_item: MenuItemCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    is_admin(user)
    new_item = MenuItem(**menu_item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"message": "Menu item added", "item": new_item}


@admin_router.put("/menu/{id}")
def update_menu_item(id: int, item_update: MenuItemCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    is_admin(user)
    item = db.query(MenuItem).filter(MenuItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    for key, value in item_update.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    return {"message": "Menu item updated",
            "item" : MenuItemResponse.model_validate(item).model_dump()}


@admin_router.delete("/menu/{id}")
def delete_menu_item(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    is_admin(user)
    item = db.query(MenuItem).filter(MenuItem.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(item)
    db.commit()
    return {"message": "Menu item removed"}


@admin_router.get("/orders", response_model=List[OrderResponse])
def view_all_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    is_admin(user)
    orders = db.query(Order).all()
    return orders
