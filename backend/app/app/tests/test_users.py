from app.tests.setup import client


def test_jwt(username: str = "admin", password: str = "admin"):
    response = client.post(
        "/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": f"{username}", "password": f"{password}"}
    )
    assert response.json().get('access_token') is not None
    assert response.status_code == 200
