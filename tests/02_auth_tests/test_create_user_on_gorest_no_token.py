import requests


def test_user_create_fails_without_a_token_v2():
    url = "https://gorest.co.in/public/v2/users"
    response = requests.post(url, '{}')
    assert response.status_code == 401
    assert response.reason == "Unauthorized"


def test_user_create_fails_without_a_token_v1():
    url = "https://gorest.co.in/public/v1/users"
    response = requests.post(url, '{}')
    assert response.status_code == 401
    assert response.reason == "Unauthorized"


def test_user_create_fails_without_a_token_public_api():
    url = "https://gorest.co.in/public-api/users"
    response = requests.post(url, '{}')
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["code"] == 401