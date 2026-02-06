from typing import List
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .base_page import BasePage


class SearchPage(BasePage):
    """Page Object для страницы поиска Читай-город"""

    # Локаторы для страницы поиска
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product-card")
    PRODUCT_TITLE = (
        By.CSS_SELECTOR, ".product-card__title, .product-title, .title"
    )
    PRODUCT_AUTHOR = (
        By.CSS_SELECTOR, ".product-card__author, .author"
    )
    PRODUCT_PRICE = (
        By.CSS_SELECTOR, ".product-card__price, .product-price, .price"
    )
    NO_RESULTS_MESSAGE = (
        By.CSS_SELECTOR, ".search-empty, .no-results, .empty-state"
    )
    SEARCH_QUERY_TEXT = (
        By.CSS_SELECTOR, ".search-title, .search-results__title, h1"
    )
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='phrase']")

    @allure.step("Получить результаты поиска")
    def get_search_results(self) -> List[WebElement]:
        """Получить все результаты поиска"""
        try:
            return self.find_elements(self.SEARCH_RESULTS, timeout=10)
        except Exception:
            return []

    @allure.step("Получить количество результатов поиска")
    def get_results_count(self) -> int:
        """Получить количество найденных товаров"""
        return len(self.get_search_results())

    @allure.step("Проверить наличие книги '{book_title}' в результатах")
    def is_book_in_results(self, book_title: str) -> bool:
        """Проверить наличие книги в результатах поиска"""
        results = self.get_search_results()
        for result in results:
            try:
                # Ищем заголовок внутри карточки товара
                title_selectors = (
                    ".product-card__title, .product-title, .title, h3, a"
                )
                title_elements = result.find_elements(
                    By.CSS_SELECTOR, title_selectors
                )

                for title_element in title_elements:
                    title_text = title_element.text.strip()
                    title_lower = title_text.lower()
                    search_lower = book_title.lower()
                    if title_text and search_lower in title_lower:
                        return True
            except Exception:
                continue
        return False

    @allure.step("Проверить сообщение 'Нет результатов'")
    def is_no_results_message_displayed(self) -> bool:
        """Проверить отображение сообщения об отсутствии результатов"""
        return self.is_element_visible(self.NO_RESULTS_MESSAGE, timeout=5)

    @allure.step("Получить текст поискового запроса на странице")
    def get_search_query_displayed(self) -> str:
        """Получить отображаемый текст поискового запроса"""
        try:
            return self.get_text(self.SEARCH_QUERY_TEXT)
        except Exception:
            return ""

    @allure.step("Получить текст в поисковой строке")
    def get_search_input_value(self) -> str:
        """Получить значение поисковой строки"""
        try:
            element = self.find_element(self.SEARCH_INPUT, timeout=5)
            return element.get_attribute("value") or ""
        except Exception:
            return ""

    @allure.step("Выбрать первый товар из результатов")
    def select_first_product(self) -> None:
        """Выбрать первый товар из результатов поиска"""
        results = self.get_search_results()
        if results:
            results[0].click()
