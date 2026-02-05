import pytest
import requests
from faker import Faker
import allure
from config.constants import LOGIN_URL, AUTH_HEADERS, AUTH_DATA, API_HEADERS

fake = Faker()


@pytest.fixture(scope="session")
def auth_session():
    with allure.step("Авторизация через API"):
        session = requests.Session()
        response = session.post(f"{LOGIN_URL}", data=AUTH_DATA, headers=AUTH_HEADERS)
        assert response.status_code == 200, f"Auth failed: {response.status_code}, {response.text}"
        token = response.json().get("access_token")
        assert token, "No access_token found"
        session.headers.update(API_HEADERS)
        session.headers.update({"Authorization": f"Bearer {token}"})
        return session


@pytest.fixture()
def item_data():
    with allure.step("Генерация данных для элемента"):
        return {
            "title": fake.word().capitalize(),
            "description": fake.sentence(nb_words=10)
        }
