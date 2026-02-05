import requests
import allure
from config.constants import ITEMS_URL
from faker import Faker

fake = Faker()

@allure.epic("Items API")
@allure.feature("CRUD operations")
class TestItems:
    @allure.story("Create item")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание нового элемента")
    @allure.description("Проверка создания элемента с валидными данными")
    def test_create_item(self, auth_session, item_data):
        with allure.step("Отправка POST запроса на /items/"):
            response = auth_session.post(ITEMS_URL, json=item_data)
        with allure.step("Проверка успешного создания"):
            assert response.status_code == 200, (
                f"Ошибка при создании элемента: {response.status_code}, {response.text}"
            )
            data = response.json()
            with allure.step("Проверка структуры ответа"):
                assert data.get("id") is not None, "ID созданного элемента не возвращается"
                assert data.get("title") == item_data["title"], "Заголовок созданного элемента не совпадает"
            TestItems.created_item_id = data.get("id")

    @allure.story("Read items")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Получение списка элементов")
    @allure.description("Проверка структуры ответа: count, data")
    def test_get_items(self, auth_session):
        params = {"limit": 5, "offset": 0}
        with allure.step("Отправка GET запроса на /items/"):
            response = auth_session.get(ITEMS_URL, params=params)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Ошибка при GET /items/: {response.status_code}"

        data = response.json()
        items_list = data.get("data", [])

        with allure.step("Проверка структуры ответа"):
            assert isinstance(items_list, list), "'data' не является списком"
            assert "count" in data, "Нет ключа 'count'"
            assert isinstance(data["count"], int), "'count' не число"
            assert len(items_list) <= 5, "Количество элементов больше лимита"

    @allure.story("Update item")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Обновление элемента")
    @allure.description("Проверка обновления существующего элемента")
    def test_update_item(self, auth_session, item_data):
        item_id = getattr(TestItems, "created_item_id", None)
        assert item_id is not None, "Нет ID элемента для обновления"
        new_data = {
            "title": item_data["title"] + " Updated",
            "description": item_data["description"] + " Updated"
        }
        with allure.step(f"Отправка PUT запроса на /items/{item_id}"):
            response = auth_session.put(f"{ITEMS_URL}{item_id}", json=new_data)
        with allure.step("Проверка ответа"):
            assert response.status_code == 200, (
                f"Ошибка при обновлении элемента: {response.status_code}, {response.text}"
            )
        data = response.json()
        with allure.step("Проверка обновлённых данных"):
            assert data["title"] == new_data["title"], "Заголовок не обновился"
            assert data["description"] == new_data["description"], "Описание не обновилось"

    @allure.story("Delete item")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Удаление элемента")
    @allure.description("Проверка успешного удаления существующего элемента")
    def test_delete_item(self, auth_session, item_data):
        with allure.step("Создание элемента"):
            response = auth_session.post(ITEMS_URL, json=item_data)
            assert response.status_code == 200
            item_id = response.json()["id"]
        with allure.step(f"Удаление элемента /items/{item_id}"):
            response = auth_session.delete(f"{ITEMS_URL}{item_id}")
            assert response.status_code == 200, (
                f"Ошибка при удалении: {response.status_code}, {response.text}"
            )

    @allure.story("Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Создание элемента с некорректными данными")
    @allure.description("Проверка валидации при пустом заголовке и None описании")
    def test_create_invalid_item(self, auth_session):
        invalid_data = {"title": "", "description": None}
        with allure.step("Отправка POST запроса с невалидными данными"):
            response = auth_session.post(ITEMS_URL, json=invalid_data)
        with allure.step("Проверка кода 422"):
            assert response.status_code == 422, (
                f"Должен быть код 422 при невалидных данных, получено {response.status_code}"
            )
            assert "detail" in response.json(), "Нет сообщения об ошибке в ответе"

    @allure.story("Security")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Доступ к API без токена")
    @allure.description("Проверка, что API возвращает 401 без токена")
    def test_access_without_token(self, item_data):
        with allure.step("Отправка POST без токена"):
            response = requests.post(ITEMS_URL, json=item_data)
        with allure.step("Проверка кода 401 при отправке POST без токена"):
            assert response.status_code == 401, f"Должен быть 401 без токена, получено {response.status_code}"
            assert "detail" in response.json(), "Нет сообщения об ошибке"
        with allure.step("Отправка GET без токена"):
            response = requests.get(ITEMS_URL)
        with allure.step("Проверка кода 401 при отправке GET без токена"):
            assert response.status_code == 401, f"GET без токена должен быть 401, получено {response.status_code}"

    @allure.story("Negative scenarios")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Обновление несуществующего элемента")
    @allure.description("Проверка ошибки при обновлении элемента с несуществующим ID")
    def test_update_nonexistent_item(self, auth_session, item_data):
        with allure.step("PUT запрос на несуществующий элемент"):
            response = auth_session.put(f"{ITEMS_URL}9999999", json=item_data)
        with allure.step("Проверка кода 422 при отправке PUT запроса на несуществующий элемент"):
            assert response.status_code == 422, (
                f"Обновление несуществующего элемента должно вернуть 422 Validation Error, "
                f"получено {response.status_code}, ответ: {response.text}"
            )

    @allure.story("Negative scenarios")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Удаление несуществующего элемента")
    @allure.description("Проверка ошибки при удалении элемента с несуществующим ID")
    def test_delete_nonexistent_item(self, auth_session):
        with allure.step("DELETE запрос на несуществующий элемент"):
            response = auth_session.delete(f"{ITEMS_URL}9999999")
        with allure.step("Проверка кода 422 при отправке DELETE запроса на несуществующий элемент"):
            assert response.status_code == 422, (
                f"Удаление несуществующего элемента должно вернуть 422 Validation Error, "
                f"получено {response.status_code}, ответ: {response.text}"
            )

    @allure.story("Delete item")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Двойное удаление элемента")
    @allure.description("Создание элемента и попытка удалить его дважды — второй раз должен вернуть 404")
    def test_double_delete(self, auth_session, item_data):
        with allure.step("Создание элемента"):
            response = auth_session.post(ITEMS_URL, json=item_data)
            item_id = response.json()["id"]
        with allure.step("Первое удаление"):
            response = auth_session.delete(f"{ITEMS_URL}{item_id}")
            assert response.status_code == 200, f"Ошибка при первом удалении: {response.status_code}"
        with allure.step("Второе удаление (должно быть 404)"):
            response = auth_session.delete(f"{ITEMS_URL}{item_id}")
            assert response.status_code == 404, f"Второе удаление должно быть 404, получено {response.status_code}"

    @allure.story("Stability")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Проверка отсутствия 500 ошибки")
    @allure.description("Проверка, что сервер не падает при некорректных данных")
    def test_no_500_on_bad_requests(self, auth_session):
        bad_data = {"title": None, "description": None}
        with allure.step("POST с некорректными данными"):
            response = auth_session.post(ITEMS_URL, json=bad_data)
        with allure.step("Проверка кода 500"):
            assert response.status_code != 500, "Сервер вернул 500 Internal Error на плохих данных"