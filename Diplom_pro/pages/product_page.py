import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductPage(BasePage):
    """Page Object для страницы товара"""

    # Locators
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product-title")
    PRODUCT_AUTHOR = (By.CSS_SELECTOR, ".product-author")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-price")
    BUY_BUTTON = (By.CSS_SELECTOR, "[data-testid='buy-button']")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".add-to-cart")
    CART_MODAL = (By.CSS_SELECTOR, ".cart-modal")

    @allure.step("Получить название товара")
    def get_product_title(self) -> str:
        """Получить название товара"""
        return self.get_text(self.PRODUCT_TITLE)

    @allure.step("Получить автора товара")
    def get_product_author(self) -> str:
        """Получить автора товара"""
        return self.get_text(self.PRODUCT_AUTHOR)

    @allure.step("Получить цену товара")
    def get_product_price(self) -> str:
        """Получить цену товара"""
        return self.get_text(self.PRODUCT_PRICE)

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self) -> None:
        """Добавить товар в корзину"""
        self.click(self.BUY_BUTTON)

    @allure.step("Проверить, что кнопка 'Купить' отображается")
    def is_buy_button_visible(self) -> bool:
        """Проверить видимость кнопки 'Купить'"""
        return self.is_element_visible(self.BUY_BUTTON)

    @allure.step("Проверить, что товар в наличии")
    def is_product_available(self) -> bool:
        """Проверить наличие товара"""
        # Если нет кнопки "Купить" или есть сообщение "Нет в наличии"
        no_stock_message = (By.CSS_SELECTOR, ".out-of-stock")
        buy_button_visible = self.is_element_visible(self.BUY_BUTTON)
        no_stock_visible = self.is_element_visible(no_stock_message)
        return buy_button_visible and not no_stock_visible
