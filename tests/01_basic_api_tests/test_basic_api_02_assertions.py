import requests


def test_myip():
    response = requests.get("https://api.ipify.org/?format=json")
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    assert data['ip'] is not None
    assert response.headers["Content-Type"] == "application/json"
