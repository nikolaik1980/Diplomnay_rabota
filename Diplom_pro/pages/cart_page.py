from typing import List
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from .base_page import BasePage


class CartPage(BasePage):
    """Page Object для страницы корзины"""

    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-item")
    ITEM_QUANTITY = (By.CSS_SELECTOR, ".quantity-input")
    ITEM_PRICE = (By.CSS_SELECTOR, ".item-price")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".total-price")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".remove-item")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".checkout-button")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, ".empty-cart")

    @allure.step("Открыть корзину")
    def open_cart(self) -> None:
        """Открыть страницу корзины"""
        self.open("/cart")
        self.wait_for_page_load()

    @allure.step("Получить товары в корзине")
    def get_cart_items(self) -> List[WebElement]:
        """Получить все товары в корзине"""
        return self.find_elements(self.CART_ITEMS)

    @allure.step("Получить количество товаров в корзине")
    def get_items_count(self) -> int:
        """Получить количество товаров в корзине"""
        return len(self.get_cart_items())

    @allure.step("Изменить количество товара на {quantity}")
    def change_item_quantity(self, item_index: int,
                             quantity: int) -> None:
        """Изменить количество товара"""
        items = self.get_cart_items()
        if item_index < len(items):
            quantity_input = items[item_index].find_element(
                *self.ITEM_QUANTITY
            )
            quantity_input.clear()
            quantity_input.send_keys(str(quantity))

    @allure.step("Получить общую сумму")
    def get_total_price(self) -> float:
        """Получить общую сумму заказа"""
        total_text = self.get_text(self.TOTAL_PRICE)
        # Извлечь число из строки
        import re
        numbers = re.findall(r"[\d.,]+", total_text)
        if numbers:
            return float(numbers[0].replace(",", "."))
        return 0.0

    @allure.step("Удалить товар из корзины")
    def remove_item(self, item_index: int) -> None:
        """Удалить товар из корзины"""
        items = self.get_cart_items()
        if item_index < len(items):
            remove_btn = items[item_index].find_element(
                *self.REMOVE_BUTTON
            )
            remove_btn.click()

    @allure.step("Перейти к оформлению заказа")
    def proceed_to_checkout(self) -> None:
        """Перейти к оформлению заказа"""
        self.click(self.CHECKOUT_BUTTON)

    @allure.step("Проверить, что корзина пуста")
    def is_cart_empty(self) -> bool:
        """Проверить, пуста ли корзина"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)
