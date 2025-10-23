import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    """Фикстура: базовый URL Postman Echo API"""
    return "https://postman-echo.com"

@pytest.fixture(scope="function")
def api_session():
    """Фикстура: сессия requests для каждого теста"""
    with requests.Session() as s:
        yield s


def test_get_simple(base_url, api_session):
    """Тест: простой GET-запрос без параметров"""
    response = api_session.get(f"{base_url}/get")
    assert response.status_code == 200,  "Ждем код ответа сервера 200"

    data = response.json()
    assert data["url"] == f"{base_url}/get"
    assert data["args"] == {}
    assert data["headers"]["host"] == "postman-echo.com"

def test_get_with_query_params(base_url, api_session):
    """Тест: GET с query-параметрами"""
    params = {"test_key": "test_value", "number": "123"}
    response = api_session.get(f"{base_url}/get", params=params)
    assert response.status_code == 200,  "Ждем код ответа сервера 200"

    data = response.json()
    assert data["args"] == params
    assert data["args"]["number"] == "123"

def test_post_json(base_url, api_session):
    """Тест: POST с JSON-телом"""
    payload = {"message": "Hello", "flag": True, "count": 100}
    response = api_session.post(f"{base_url}/post", json=payload)
    assert response.status_code == 204,  "Ждем код ответа сервера 200"

    data = response.json()
    assert data["json"] == payload

def test_post_form_data(base_url, api_session):
    """Тест: POST с form-encoded данными"""
    form_data = {"username": "pytest_user", "role": "tester"}
    response = api_session.post(f"{base_url}/post", data=form_data)
    assert response.status_code == 200,  "Ждем код ответа сервера 200"

    data = response.json()
    assert data["form"] == form_data

def test_custom_header_in_request(base_url,api_session):
    """Тест: запрос с кастомным заголовком"""
    headers = {"X-Test-Client": "pytest-automation"}
    response = api_session.post(f"{base_url}/post", json={}, headers=headers)
    assert response.status_code == 200,  "Ждем код ответа сервера 200"

    data = response.json()
    assert "x-test-client" in data["headers"]
    assert data["headers"]["x-test-client"] == "pytest-automation"