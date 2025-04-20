import pytest

from app.models import MenuItem, Order, User

def test_browse_menu(authenticated_user_client, db):
    menu_item1 = MenuItem(name = "Burger", price=100)
    menu_item2 = MenuItem(name = "Pizza", price=200)

    db.add_all([menu_item1, menu_item2])
    db.commit()

    response = authenticated_user_client.get("/menu")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2


def test_place_order_success(authenticated_user_client, db):
    menu_item1 = MenuItem(name="Burger", price=100)

    db.add(menu_item1)
    db.commit()

    response = authenticated_user_client.post("/order", json={
        "menu_id" : menu_item1.id,
        "quantity" : 2
    })

    data = response.json()
    assert response.status_code == 200
    assert data["menu_id"] == menu_item1.id
    assert data["quantity"] == 2


def test_unauthenticated_user_cannot_place_order(client, db):
    menu_item1 = MenuItem(name="Burger", price=100)

    db.add(menu_item1)
    db.commit()

    response = client.post("/order", json={
        "menu_id" : menu_item1.id,
        "quantity" : 2
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_user_cancel_order(authenticated_user_client, db):
    user = db.query(User).filter_by(username="TestUser").first()
    menu_item = MenuItem(name="Burger", price=100)
    order = Order(user_id = user.id, menu_id = menu_item.id, quantity =2)
    
    db.add(order)
    db.commit()
    db.refresh(order)

    response = authenticated_user_client.delete(f"/order/{order.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Order cancelled"


def test_cancel_order_not_founrd(authenticated_user_client, db):
    user1 = User(username="user1", email="user1@example.com", password_hash="user1")
    db.add(user1)
    db.commit()
    db.refresh(user1)

    item = MenuItem(name="Burger", price=100.0)
    db.add(item)
    db.commit()
    db.refresh(item)

    order = Order(user_id=user1.id, menu_id=item.id, quantity=1)
    db.add(order)
    db.commit()
    db.refresh(order)

    response = authenticated_user_client.delete(f"/order/{order.id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"


def test_get_order_history(authenticated_user_client, db):
    user = db.query(User).filter_by(username="TestUser").first()

    item1 = MenuItem(name="Pizza", price=150.0)
    item2 = MenuItem(name="Burger", price=100.0)
    db.add_all([item1, item2])
    db.commit()
    db.refresh(item1)
    db.refresh(item2)

    order1 = Order(user_id=user.id, menu_id=item1.id, quantity=1)
    order2 = Order(user_id=user.id, menu_id=item2.id, quantity=2)
    db.add_all([order1, order2])
    db.commit()

    response = authenticated_user_client.get("/orders/history")
    orders = response.json()

    assert response.status_code == 200
    assert len(orders) == 2


def test_unauthenticated_user_cannot_access_order_history(client):
    response = client.get("/orders/history")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"



# @pytest.mark.user
# @pytest.mark.asyncio
# async def test_view_order_history(authenticated_user_client):
#     response = await authenticated_user_client.get("/orders/history")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)


# @pytest.mark.user
# @pytest.mark.parametrize("invalid_data", [
#     {"quantity": 2},  # Missing menu_id
#     {"menu_id": 1},  # Missing quantity
#     {"menu_id": 1, "quantity": "two"},  # Invalid quantity type
# ])
# def test_place_order_invalid(client, invalid_data):
#     response = client.post(
#         "/order",
#         json=invalid_data,
#         headers={"Authorization": "Bearer user_token"},
#     )
#     assert response.status_code == 422


# @pytest.mark.user
# def test_cancel_order(client):
#     client.post(
#         "/order",
#         json={"menu_id": 1, "quantity": 1},
#         headers={"Authorization": "Bearer user_token"},
#     )
#     response = client.delete("/order/1", headers={"Authorization": "Bearer user_token"})
#     assert response.status_code == 200
