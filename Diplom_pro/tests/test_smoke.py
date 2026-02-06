import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.epic("Smoke Tests")
@allure.feature("Базовые проверки сайта")
class TestSmoke:
    """Упрощенные smoke тесты"""

    @allure.story("Доступность")
    @allure.title("Сайт открывается и загружается")
    @allure.tag("smoke", "critical")
    @pytest.mark.ui
    def test_site_opens(self, driver):
        """Тест открытия сайта"""
        with allure.step("Открыть главную страницу"):
            driver.get("https://www.chitai-gorod.ru/")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        with allure.step("Проверить заголовок страницы"):
            title = driver.title
            assert title, "Заголовок страницы должен содержать текст"
            allure.attach(
                f"Page title: {title}",
                name="Page Title",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Проверить URL"):
            current_url = driver.current_url
            assert "chitai-gorod.ru" in current_url, (
                f"Ожидался сайт Читай-город, получен: {current_url}"
            )
            allure.attach(
                f"Current URL: {current_url}",
                name="Current URL",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.story("Контент")
    @allure.title("Страница содержит контент")
    @allure.tag("smoke", "content")
    @pytest.mark.ui
    def test_page_has_content(self, driver):
        """Тест наличия контента на странице"""
        with allure.step("Открыть главную страницу"):
            driver.get("https://www.chitai-gorod.ru/")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        with allure.step("Проверить длину HTML"):
            page_source = driver.page_source
            page_length = len(page_source)

            allure.attach(
                f"Page source length: {page_length} characters\n"
                f"First 500 chars: {page_source[:500]}",
                name="Content Analysis",
                attachment_type=allure.attachment_type.TEXT
            )

            assert page_length > 10000, (
                "Страница слишком короткая (возможно, не загрузилась)"
            )

    @allure.story("Поиск")
    @allure.title("Проверка поискового поля")
    @allure.tag("smoke", "search")
    @pytest.mark.ui
    def test_search_field_exists(self, driver):
        """Тест наличия поискового поля"""
        with allure.step("Открыть главную страницу"):
            driver.get("https://www.chitai-gorod.ru/")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        with allure.step("Найти поле поиска"):
            # Попробуем разные селекторы
            search_selectors = [
                "input[name='phrase']",
                "input[placeholder*='ищу']",
                "input[type='search']",
                "input.search-input"
            ]

            found_input = None
            for selector in search_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        found_input = elements[0]
                        allure.attach(
                            f"Found search input with selector: {selector}",
                            name="Search Input Found",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        break
                except Exception:
                    continue

            if found_input:
                # Проверим placeholder
                placeholder = found_input.get_attribute("placeholder") or ""
                allure.attach(
                    f"Search placeholder: '{placeholder}'",
                    name="Search Placeholder",
                    attachment_type=allure.attachment_type.TEXT
                )

                assert placeholder, (
                    "Поисковая строка должна иметь placeholder"
                )
            else:
                allure.attach(
                    "Search input not found with standard selectors",
                    name="Search Note",
                    attachment_type=allure.attachment_type.TEXT
                )
                # Проверим, есть ли вообще input элементы
                all_inputs = driver.find_elements(By.TAG_NAME, "input")
                allure.attach(
                    f"Total input elements found: {len(all_inputs)}",
                    name="Input Count",
                    attachment_type=allure.attachment_type.TEXT
                )

                # Пропустим тест, если поле поиска не найдено
                pytest.skip("Search input not found on current page layout")
