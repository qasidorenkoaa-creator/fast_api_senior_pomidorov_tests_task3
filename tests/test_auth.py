import requests
import allure
from config.constants import LOGIN_URL, AUTH_HEADERS, AUTH_DATA


@allure.epic("Authorization API")
@allure.feature("Login")
class TestAuth:

    @allure.story("Получение access_token")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Успешная авторизация пользователя")
    @allure.description("Проверка получения access_token с валидными учетными данными")
    def test_auth(self):
        with allure.step("Отправка POST запроса на /login"):
            response = requests.post(LOGIN_URL, data=AUTH_DATA, headers=AUTH_HEADERS)
        with allure.step("Проверка ответа сервера"):
            assert response.status_code == 200
        with allure.step("Проверка наличия access_token"):
            assert "access_token" in response.json()
