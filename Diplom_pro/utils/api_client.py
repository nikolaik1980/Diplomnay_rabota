import requests
import allure
from typing import Dict, Any, Optional


class APIClient:
    """Клиент для работы с API"""

    def __init__(self):
        self.base_url = "https://www.chitai-gorod.ru"
        self.timeout = 10
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/html, */*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        })

    @allure.step("Отправить GET запрос к {endpoint}")
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """Отправить GET запрос"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {**self.session.headers, **(headers or {})}

        with allure.step(f"GET запрос: {url}"):
            with allure.step(f"Параметры: {params}"):
                try:
                    response = self.session.get(
                        url,
                        params=params,
                        headers=request_headers,
                        timeout=self.timeout
                    )
                except Exception as e:
                    allure.attach(
                        f"Request failed: {str(e)}",
                        name="Request Error",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    raise

        allure.attach(
            f"Request URL: {response.request.url}\n"
            f"Request Method: {response.request.method}\n"
            f"Response Status: {response.status_code}\n"
            f"Response Headers: {dict(response.headers)}\n"
            f"Response Body (first 1000 chars): {response.text[:1000]}",
            name="API Request/Response",
            attachment_type=allure.attachment_type.TEXT
        )

        return response

    @allure.step("Поиск книг по запросу '{phrase}'")
    def search_books(self, phrase: str) -> requests.Response:
        """Поиск книг через сайт"""
        # Используем поиск на основном сайте
        return self.get("/search", params={"q": phrase})

    @allure.step("Проверить успешный ответ API")
    def assert_success_response(self, response: requests.Response,
                                expected_codes: list = None) -> None:
        """Проверить успешный ответ API"""
        expected_codes = expected_codes or [200]
        assert response.status_code in expected_codes, (
            f"Expected status code in {expected_codes}, "
            f"got {response.status_code}"
        )

    @allure.step("Проверить, что ответ содержит данные")
    def assert_response_contains_data(self,
                                      response: requests.Response) -> None:
        """Проверить, что ответ содержит данные"""
        assert len(response.text) > 0, "Response body is empty"
        assert response.headers.get('Content-Type', ''), (
            "Response has no Content-Type"
        )
