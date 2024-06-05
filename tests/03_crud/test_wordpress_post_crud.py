import time
from base64 import b64encode
import requests
import pytest
import lorem


# GLOBAL VARIABLES
username = 'editor'
password = 'HWZg hZIP jEfK XCDE V9WM PQ3t'
blog_url = 'https://gaworski.net'
posts_endpoint_url = blog_url + "/wp-json/wp/v2/posts"
token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")


@pytest.fixture(scope='module')
def article():
    timestamp = int(time.time())
    article = {
        "article_creation_date": timestamp,
        "article_title": "This is new post " + str(timestamp),
        "article_subtitle": lorem.sentence(),
        "article_text": lorem.paragraph()
    }
    return article


@pytest.fixture(scope='module')
def headers():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + token
    }
    return headers


@pytest.fixture(scope='module')
def posted_article(article, headers):
    payload = {
        "title": article["article_title"],
        "excerpt": article["article_subtitle"],
        "content": article["article_text"],
        "status": "publish"
    }
    print(payload["title"])
    response = requests.post(url=posts_endpoint_url, headers=headers, json=payload)
    return response


# CREATE
def test_new_post_is_successfully_created(posted_article):
    assert posted_article.status_code == 201
    assert posted_article.reason == "Created"


# READ
def test_newly_created_post_can_be_read(article, posted_article):
    wordpress_post_id = posted_article.json()["id"]
    wordpress_post_url = f'{posts_endpoint_url}/{wordpress_post_id}'
    published_article = requests.get(url=wordpress_post_url)
    assert published_article.status_code == 200
    assert published_article.reason == "OK"
    wordpress_post_data = published_article.json()
    assert wordpress_post_data["title"]["rendered"] == article["article_title"]
    assert wordpress_post_data["excerpt"]["rendered"] == f'<p>{article["article_subtitle"]}</p>\n'
    assert wordpress_post_data["content"]["rendered"] == f'<p>{article["article_text"]}</p>\n'
    assert wordpress_post_data["status"] == 'publish'


# UPDATE
def test_post_can_be_updated(article, posted_article, headers):
    wordpress_post_id = posted_article.json()["id"]
    wordpress_post_url = posts_endpoint_url + "/" + str(wordpress_post_id)
    payload = {
        "excerpt": "This is new excerpt!"
    }
    updated_article = requests.patch(url=wordpress_post_url, json=payload, headers=headers)
    assert updated_article.status_code == 200
    assert updated_article.reason == "OK"
    published_article = requests.get(url=wordpress_post_url)
    wordpress_post_data = published_article.json()
    assert wordpress_post_data["excerpt"]["rendered"] == f'<p>{payload["excerpt"]}</p>\n'
    assert wordpress_post_data["title"]["rendered"] == article["article_title"]
    assert wordpress_post_data["content"]["rendered"] == f'<p>{article["article_text"]}</p>\n'
    assert wordpress_post_data["status"] == 'publish'


def test_post_can_be_deleted(posted_article, headers):
    wordpress_post_id = posted_article.json()["id"]
    wordpress_post_url = posts_endpoint_url + "/" + str(wordpress_post_id)
    wordpress_delete_post_url = wordpress_post_url + "?force=true"
    deleted_article = requests.delete(url=wordpress_delete_post_url, headers=headers)
    assert deleted_article.status_code == 200
    assert deleted_article.reason == "OK"
    published_article = requests.get(url=wordpress_post_url)
    assert published_article.status_code == 404
    assert published_article.reason == "Not Found"