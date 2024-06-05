import pytest
import requests


@pytest.fixture(scope='module')
def myip():
    url = "https://api.ipify.org/?format=json"
    response = requests.get(url)
    return response


def test_my_ip_request_status_is200(myip):
    assert myip.status_code == 200


def test_my_ip_request_has_a_body(myip):
    data = myip.json()
    assert data is not None
    assert data['ip'] is not None


def test_my_ip_has_json_header(myip):
    assert myip.headers["Content-Type"] == "application/json"
