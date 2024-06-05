import requests


def test_my_ip_request_status_is200():
    url = "https://api.ipify.org/?format=json"
    response = requests.get(url)
    assert response.status_code == 200


def test_my_ip_request_has_a_body():
    url = "https://api.ipify.org/?format=json"
    response = requests.get(url)
    data = response.json()
    assert data is not None
    assert data['ip'] is not None


def test_my_ip_has_json_header():
    url = "https://api.ipify.org/?format=json"
    response = requests.get(url)
    assert response.headers["Content-Type"] == "application/json"
