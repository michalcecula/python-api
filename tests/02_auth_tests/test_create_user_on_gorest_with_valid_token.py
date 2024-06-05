from faker import Faker
import requests
from random import choice


def test_user_create_pass_with_valid_token_v2():
    url = "https://gorest.co.in/public/v2/users"
    headers = {
        "Authorization": "Bearer 41a9e72c965f84ff57957a078052d66f1af3296ba51d9caf5615a3fa5c51f855"
    }
    user_data = {
        "name": Faker().name(),
        "gender": choice(["male", "female"]),
        "email": Faker().email(),
        "status": "active"
    }
    response_post = requests.post(url, data=user_data, headers=headers)
    assert response_post.status_code == 201
    assert response_post.reason == "Created"
    user_id = response_post.json()['id']
    response_get = requests.get(url + "/" + str(user_id), headers=headers)
    assert response_get.status_code == 200
    assert response_get.reason == 'OK'
    received_data = response_get.json()
    assert user_data["name"] == received_data["name"]
    assert user_data["gender"] == received_data["gender"]
    assert user_data["email"] == received_data["email"]
    assert user_data["status"] == received_data["status"]


def test_user_create_pass_with_valid_token_v1():
    url = "https://gorest.co.in/public/v1/users"
    headers = {
        "Authorization": "Bearer 41a9e72c965f84ff57957a078052d66f1af3296ba51d9caf5615a3fa5c51f855"
    }
    user_data = {
        "name": Faker().name(),
        "gender": choice(["male", "female"]),
        "email": Faker().email(),
        "status": "active"
    }
    response_post = requests.post(url, data=user_data, headers=headers)
    assert response_post.status_code == 201
    assert response_post.reason == "Created"
    user_id = response_post.json()['data']['id']
    response_get = requests.get(url + "/" + str(user_id), headers=headers)
    assert response_get.status_code == 200
    assert response_get.reason == 'OK'
    received_data = response_get.json()['data']
    assert user_data["name"] == received_data["name"]
    assert user_data["gender"] == received_data["gender"]
    assert user_data["email"] == received_data["email"]
    assert user_data["status"] == received_data["status"]


def test_user_create_pass_with_valid_token_public_api():
    url = "https://gorest.co.in/public-api/users"
    headers = {
        "Authorization": "Bearer 41a9e72c965f84ff57957a078052d66f1af3296ba51d9caf5615a3fa5c51f855"
    }
    user_data = {
        "name": Faker().name(),
        "gender": choice(["male", "female"]),
        "email": Faker().email(),
        "status": "active"
    }
    response_post = requests.post(url, data=user_data, headers=headers)
    assert response_post.status_code == 200
    json_post_response = response_post.json()
    assert json_post_response['code'] == 201
    user_id = json_post_response['data']['id']
    response_get = requests.get(url + "/" + str(user_id), headers=headers)
    assert response_get.status_code == 200
    assert response_get.json()['code'] == 200
    received_data = response_get.json()['data']
    assert user_data["name"] == received_data["name"]
    assert user_data["gender"] == received_data["gender"]
    assert user_data["email"] == received_data["email"]
    assert user_data["status"] == received_data["status"]