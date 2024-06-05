import requests


def test_myip():
    response = requests.get("https://api.ipify.org/?format=json")
    assert response.status_code == 200

