BASE_URL = "https://fast-api.senior-pomidorov.ru"

LOGIN_URL = f"{BASE_URL}/api/v1/login/access-token"
ITEMS_URL = f"{BASE_URL}/api/v1/items/"

AUTH_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json"
}

API_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

AUTH_DATA = {
    "username": "qa.sidorenko.aa@gmail.com",
    "password": "Pomidor1111",
    "scope": "",
    "client_id": "",
    "client_secret": ""
}
