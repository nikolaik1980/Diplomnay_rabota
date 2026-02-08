from typing import Optional, Tuple, List
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Базовый класс для всех Page Object"""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.base_url = "https://www.chitai-gorod.ru"

    @allure.step("Открыть страницу {url}")
    def open(self, url: str = "") -> None:
        """Открыть указанный URL"""
        if url:
            full_url = f"{self.base_url}/{url.lstrip('/')}"
        else:
            full_url = self.base_url
        self.driver.get(full_url)

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator: Tuple[str, str],
                     timeout: Optional[int] = None) -> WebDriver:
        """Найти элемент с ожиданием"""
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Найти элементы {locator}")
    def find_elements(self, locator: Tuple[str, str],
                      timeout: Optional[int] = None) -> List[WebDriver]:
        """Найти несколько элементов с ожиданием"""
        wait_time = timeout or self.timeout
        return WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_all_elements_located(locator)
        )

    @allure.step("Кликнуть на элемент {locator}")
    def click(self, locator: Tuple[str, str]) -> None:
        """Кликнуть на элемент"""
        element = self.find_element(locator)
        element.click()

    @allure.step("Ввести текст '{text}' в элемент {locator}")
    def type_text(self, locator: Tuple[str, str], text: str) -> None:
        """Ввести текст в поле"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Получить текст элемента"""
        element = self.find_element(locator)
        return element.text.strip()

    @allure.step("Проверить, что элемент {locator} отображается")
    def is_element_visible(self, locator: Tuple[str, str],
                           timeout: Optional[int] = None) -> bool:
        """Проверить видимость элемента"""
        try:
            wait_time = timeout or self.timeout
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Проверить, что элемент содержит текст")
    def assert_text_in_element(self, locator: Tuple[str, str],
                               expected_text: str) -> None:
        """Проверить текст элемента"""
        actual_text = self.get_text(locator)
        error_msg = (
            f"Expected text '{expected_text}' not found in element. "
            f"Actual: '{actual_text}'"
        )
        assert expected_text in actual_text, error_msg

    @allure.step("Сделать скриншот")
    def take_screenshot(self, name: str) -> None:
        """Сделать скриншот"""
        self.driver.save_screenshot(f"screenshots/{name}.png")

    @allure.step("Подождать загрузки страницы")
    def wait_for_page_load(self, timeout: int = 10) -> None:
        """Ожидать загрузки страницы"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script(
                    "return document.readyState"
                ) == "complete"
            )
        except TimeoutException:
            print(f"Page load timeout after {timeout} seconds")

    @allure.step("Получить атрибут элемента {locator}")
    def get_attribute(self, locator: Tuple[str, str],
                      attribute: str) -> str:
        """Получить значение атрибута элемента"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)
