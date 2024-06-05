from faker import Faker
import pytest
import requests
from random import choice


base_url = "https://gorest.co.in/public/v2/users"
token = "41a9e72c965f84ff57957a078052d66f1af3296ba51d9caf5615a3fa5c51f855"
headers = {"Authorization": "Bearer " + token}


@pytest.fixture(scope='module')
def user_data():
    return {
        "name": Faker().name(),
        "gender": choice(["male", "female"]),
        "email": Faker().email(),
        "status": "active"
    }


@pytest.fixture(scope='module')
def create_response(user_data):
    return requests.post(base_url, data=user_data, headers=headers)


def test_user_can_be_created_with_valid_token(create_response):
    assert create_response.status_code == 201
    assert create_response.reason == "Created"


def test_user_can_be_retrieved_after_they_were_created(user_data, create_response):
    user_id = create_response.json()['id']
    response_get = requests.get(base_url + "/" + str(user_id), headers=headers)
    received_data = response_get.json()
    assert response_get.status_code == 200
    assert response_get.reason == 'OK'
    assert user_data["name"] == received_data["name"]
    assert user_data["gender"] == received_data["gender"]
    assert user_data["email"] == received_data["email"]
    assert user_data["status"] == received_data["status"]