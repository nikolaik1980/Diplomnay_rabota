import pytest
import allure
import time


@allure.epic("API Тесты")
@allure.feature("Финальные API тесты для Читай-город")
class TestAPIFinal:
    """Финальные API тесты"""

    @allure.story("Заголовки ответа")
    @allure.title("Проверка основных заголовков ответа")
    @allure.tag("api", "headers", "security")
    @pytest.mark.api
    def test_response_headers(self, api_client):
        """Тест проверки заголовков ответа"""
        with allure.step("Запросить главную страницу"):
            response = api_client.get("/")

        with allure.step("Проверить обязательные заголовки"):
            headers = response.headers

            # Сохраним заголовки для отчета
            headers_text = "\n".join(
                [f"{k}: {v}" for k, v in headers.items()]
            )
            allure.attach(
                headers_text, name="Response Headers",
                attachment_type=allure.attachment_type.TEXT
            )

            # Обязательные заголовки
            assert "Content-Type" in headers, "Missing Content-Type header"
            assert "Date" in headers, "Missing Date header"

            # Проверить Content-Type
            content_type = headers.get('Content-Type', '').lower()
            text_html_check = 'text/html' in content_type
            charset_check = 'charset=utf-8' in content_type
            content_check = text_html_check or charset_check
            assert content_check, f"Unexpected Content-Type: {content_type}"

    @allure.story("Содержимое ответа")
    @allure.title("Ответ содержит ключевые элементы сайта")
    @allure.tag("api", "content", "validation")
    @pytest.mark.api
    def test_response_content_structure(self, api_client):
        """Тест структуры содержимого ответа"""
        with allure.step("Запросить главную страницу"):
            response = api_client.get("/")
            response_text = response.text.lower()

        with allure.step("Проверить наличие ключевых элементов"):
            # Ключевые слова, которые должны быть на главной странице
            required_keywords = [
                "читай",  # часть названия сайта
                "книг",  # упоминание книг
                "html",  # HTML структура
                "<body",  # тег body
            ]

            found_keywords = []
            missing_keywords = []

            for keyword in required_keywords:
                if keyword in response_text:
                    found_keywords.append(keyword)
                else:
                    missing_keywords.append(keyword)

            allure.attach(
                f"Found keywords: {found_keywords}\n"
                f"Missing keywords: {missing_keywords}\n"
                f"Response length: {len(response_text)} characters",
                name="Content Analysis",
                attachment_type=allure.attachment_type.TEXT
            )

            # Должны быть найдены основные ключевые слова
            min_keywords = 2
            assert len(found_keywords) >= min_keywords, (
                f"Too few required keywords found. Found: {found_keywords}"
            )

    @allure.story("Производительность")
    @allure.title("Время ответа в пределах нормы")
    @allure.tag("api", "performance", "critical")
    @pytest.mark.api
    def test_response_time_performance(self, api_client):
        """Тест производительности (времени ответа)"""
        with allure.step("Измерить время ответа для главной страницы"):
            start_time = time.time()
            response = api_client.get("/")
            end_time = time.time()

            response_time = end_time - start_time

        with allure.step("Проверить время ответа"):
            allure.attach(
                f"Response time: {response_time:.3f} seconds\n"
                f"Status code: {response.status_code}\n"
                f"Response size: {len(response.text)} characters",
                name="Performance Metrics",
                attachment_type=allure.attachment_type.TEXT
            )

            # Критерии приемлемого времени ответа
            assert response_time < 10.0, (
                f"Response too slow: {response_time:.3f} seconds"
            )

            assert response.status_code == 200, (
                f"Request failed with status: {response.status_code}"
            )

            # Дополнительно: проверить размер ответа
            assert len(response.text) > 10000, (
                "Response too small, might be incomplete"
            )

    @allure.story("Поисковые запросы")
    @allure.title("Поисковые запросы обрабатываются")
    @allure.tag("api", "search", "functional")
    @pytest.mark.api
    @pytest.mark.parametrize("search_query", [
        "книги",
        "романы",
        "детективы",
    ])
    def test_search_queries_processing(self, api_client,
                                       search_query: str):
        """Тест обработки поисковых запросов"""
        with allure.step(f"Выполнить поиск по запросу '{search_query}'"):
            response = api_client.get(
                "/search", params={"phrase": search_query}
            )

        with allure.step("Проверить ответ"):
            # Поиск может вернуть 200, 30x или даже 404
            valid_statuses = [200, 301, 302, 404]
            assert response.status_code in valid_statuses, (
                f"Unexpected status for search: {response.status_code}"
            )

            # Проверить содержимое
            if response.status_code == 200:
                assert len(response.text) > 0, (
                    "Search response should not be empty"
                )

                # Проверить, что поисковый запрос упоминается в ответе
                response_text = response.text.lower()
                if search_query.lower() in response_text:
                    allure.attach(
                        f"Search query '{search_query}' found in response",
                        name="Search Query Found",
                        attachment_type=allure.attachment_type.TEXT
                    )
                else:
                    # Это нормально, если запрос не найден в ответе
                    allure.attach(
                        f"Search query '{search_query}' not in response",
                        name="Search Query Note",
                        attachment_type=allure.attachment_type.TEXT
                    )

    @allure.story("Обработка ошибок")
    @allure.title("Невалидные запросы обрабатываются корректно")
    @allure.tag("api", "error-handling", "negative")
    @pytest.mark.api
    def test_error_handling(self, api_client):
        """Тест обработки невалидных запросов"""
        with allure.step("Запросить несуществующую страницу"):
            response = api_client.get("/nonexistent-page-12345")

        with allure.step("Проверить обработку ошибки"):
            # Несуществующая страница может вернуть 404 или редирект
            valid_statuses = [404, 301, 302, 200]
            error_message = (
                f"Unexpected status for non-existent page: "
                f"{response.status_code}"
            )
            assert response.status_code in valid_statuses, error_message

            allure.attach(
                f"Status code for non-existent page: {response.status_code}\n"
                f"Response length: {len(response.text)} characters",
                name="Error Handling Info",
                attachment_type=allure.attachment_type.TEXT
            )
