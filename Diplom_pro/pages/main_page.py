import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class MainPage(BasePage):
    """Page Object для главной страницы Читай-город"""

    # Уточненные локаторы на основе отладки
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='phrase']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    PRODUCT_CARD = (By.CSS_SELECTOR, ".product-card")
    HEADER_LOGO = (By.CSS_SELECTOR, "[class*='logo'], a[href='/']")
    CART_BUTTON = (By.CSS_SELECTOR, "[href*='cart']")

    @allure.step("Открыть главную страницу")
    def open_main_page(self) -> None:
        """Открыть главную страницу"""
        self.open("")
        self.wait_for_page_load()

    @allure.step("Выполнить поиск по запросу '{query}'")
    def search_for(self, query: str) -> None:
        """Выполнить поиск товара"""
        try:
            # Найти поисковую строку с ожиданием
            search_input = self.wait.until(
                EC.presence_of_element_located(self.SEARCH_INPUT)
            )
            search_input.clear()
            search_input.send_keys(query)

            # Попробовать нажать кнопку поиска
            try:
                search_button = self.driver.find_element(*self.SEARCH_BUTTON)
                search_button.click()
            except NoSuchElementException:
                # Если кнопка не найдена, нажать Enter
                search_input.send_keys(Keys.ENTER)

            # Ожидать загрузки результатов поиска
            self.wait_for_page_load()

        except Exception as e:
            allure.attach(
                f"Search error: {str(e)}",
                name="Search Error",
                attachment_type=allure.attachment_type.TEXT
            )
            # Если поиск не работает, просто перейдем на страницу поиска
            search_url = f"{self.base_url}/search?phrase={query}"
            self.driver.get(search_url)
            self.wait_for_page_load()

    @allure.step("Получить placeholder поисковой строки")
    def get_search_placeholder(self) -> str:
        """Получить placeholder поисковой строки"""
        try:
            element = self.find_element(self.SEARCH_INPUT)
            return element.get_attribute("placeholder") or ""
        except Exception:
            return ""

    @allure.step("Проверить наличие поисковой строки")
    def is_search_input_visible(self) -> bool:
        """Проверить видимость поисковой строки"""
        return self.is_element_visible(self.SEARCH_INPUT)

    @allure.step("Получить количество товаров на странице")
    def get_product_count(self) -> int:
        """Получить количество товаров на странице"""
        try:
            products = self.find_elements(self.PRODUCT_CARD)
            return len(products)
        except Exception:
            return 0

    @allure.step("Получить заголовок страницы")
    def get_page_title(self) -> str:
        """Получить заголовок страницы"""
        return self.driver.title

    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        """Получить текущий URL"""
        return self.driver.current_url

    @allure.step("Проверить наличие логотипа")
    def is_logo_visible(self) -> bool:
        """Проверить видимость логотипа"""
        try:
            # Попробуем разные селекторы для логотипа с таймаутом
            selectors = [
                "img[alt*='Читай']",
                "img[alt*='город']",
                "a[href='/'] img",
                "[class*='logo']",
                ".header-logo",
                ".site-logo"
            ]

            for selector in selectors:
                try:
                    element = self.driver.find_element(
                        By.CSS_SELECTOR, selector
                    )
                    if element.is_displayed():
                        return True
                except Exception:
                    continue

            # Если не нашли изображение, ищем ссылку на главную
            try:
                home_link = self.driver.find_element(
                    By.CSS_SELECTOR, "a[href='/']"
                )
                return home_link.is_displayed()
            except Exception:
                return False

        except Exception as e:
            allure.attach(
                f"Logo check error: {str(e)}",
                name="Logo Error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False
