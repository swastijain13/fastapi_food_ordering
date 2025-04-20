import pytest
from app.models import MenuItem, Order, User
from app.routes.auth import get_password_hash

@pytest.mark.admin
def test_add_menu_item_success(authenticated_admin_client):
    response = authenticated_admin_client.post("/admin/menu", json={
        "name": "Burger",
        "price": 120.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Menu item added"
    assert data["item"]["name"] == "Burger"
    assert data["item"]["price"] == 120.0


def test_add_menu_item_fail(authenticated_user_client):
    response = authenticated_user_client.post("/admin/menu", json={
        "name": "Burger",
        "price": 120.0
    })

    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized"


def test_update_menu_item_success(authenticated_admin_client):
    create_response = authenticated_admin_client.post("/admin/menu", json={
        "name": "Pizza",
        "price": 250.0
    })

    item_id = create_response.json()["item"]["id"]
    update_response = authenticated_admin_client.put(f"/admin/menu/{item_id}", json={
        "name": "Pizza",
        "price": 200.0
    })

    updated_item = update_response.json()["item"]
    assert update_response.status_code == 200
    assert updated_item["price"] == 200.0


def test_update_menu_item_not_found(authenticated_admin_client):
    response = authenticated_admin_client.put("/admin/menu/9999", json={
        "name": "blank dish",
        "price": 100
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Menu item not found"


def test_view_all_orders_as_admin(authenticated_admin_client, db):
    user = User(username="testuser", email="test@example.com", password_hash=get_password_hash("testpass"))
    db.add(user)
    db.commit()
    db.refresh(user)

    menu_item = MenuItem(name="Pizza", price=200.0)
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    
    order1 = Order(user_id=user.id, menu_id=menu_item.id, quantity=1)
    order2 = Order(user_id=user.id, menu_id=menu_item.id, quantity=2)

    db.add_all([order1, order2])
    db.commit()

    response = authenticated_admin_client.get("/admin/orders")
    data = response.json()

    assert response.status_code == 200
    assert len(data) >= 2


def test_view_all_orders_unauthorized(authenticated_user_client):
    response = authenticated_user_client.get("/admin/orders")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized"


def test_delete_menu_item_success(authenticated_admin_client, db):
    item = MenuItem(name="Pizza", price=250.0)
    db.add(item)
    db.commit()
    db.refresh(item)

    response = authenticated_admin_client.delete(f"/admin/menu/{item.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Menu item removed"

