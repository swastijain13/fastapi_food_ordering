#SIGNUP TESTS
def test_signup_success(client):
    response = client.post("/auth/signup", json={
        "username": "testuser",
        "password": "testpass",
        "email": "test@example.com"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}


def test_signup_existing_user(client):
    client.post("/auth/signup", json = {
        "username" : "user1",
        "password" : "user1",
        "email" : "user1@xample.com"
    })

    response = client.post("/auth/signup", json={
        "username" : "user1",
        "password" : "new_passsword",
        "email" : "user1@example.com"
    })

    assert response.status_code == 400
    assert response.json() == {"detail" : "Username or email already taken"}



#LOGIN TESTS
def test_login_success(client, db):
    client.post("/auth/signup", json={
        "username" : "user2",
        "password" : "user2",
        "email" : "user2@example.com"
    })


    response = client.post("/auth/login", data={
        "username" : "user2",
        "password":"user2"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_wrong_password(client, db):
    client.post("/auth/signup", json={
        "username": "user3",
        "password": "user3",
        "email": "user3@example.com"
    })

    response = client.post("/auth/login", data={
        "username": "user3",
        "password": "wrongpass"
    })

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
