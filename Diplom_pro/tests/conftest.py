import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def browser_type(request):
    """Тип браузера"""
    return request.config.getoption("--browser", default="chrome")


@pytest.fixture(scope="session")
def headless(request):
    """Режим headless"""
    return request.config.getoption("--headless", default=False)


@pytest.fixture(scope="session")
def base_url(request):
    """Базовый URL"""
    return request.config.getoption(
        "--base-url", default="https://www.chitai-gorod.ru"
    )


@pytest.fixture
def driver(browser_type, headless, base_url):
    """Фикстура для создания WebDriver"""
    driver = None

    if browser_type.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(
                service=service, options=chrome_options
            )
        except Exception as e:
            print(f"Chrome driver error: {e}")
            # Попробуем без webdriver-manager
            try:
                driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                pytest.fail(f"Failed to start Chrome: {e2}")

    elif browser_type.lower() == "firefox":
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        try:
            from webdriver_manager.firefox import GeckoDriverManager
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(
                service=service, options=firefox_options
            )
        except Exception as e:
            print(f"Firefox driver error: {e}")
            try:
                driver = webdriver.Firefox(options=firefox_options)
            except Exception as e2:
                pytest.fail(f"Failed to start Firefox: {e2}")

    else:
        raise ValueError(f"Unsupported browser: {browser_type}")

    driver.implicitly_wait(10)

    # Не максимизируем окно в headless режиме
    if not headless:
        driver.maximize_window()

    yield driver

    if driver:
        driver.quit()


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    from utils.api_client import APIClient
    return APIClient()


@pytest.fixture
def main_page(driver):
    """Фикстура для главной страницы"""
    from pages.main_page import MainPage
    return MainPage(driver)


@pytest.fixture
def search_page(driver):
    """Фикстура для страницы поиска"""
    from pages.search_page import SearchPage
    return SearchPage(driver)


@pytest.fixture
def product_page(driver):
    """Фикстура для страницы товара"""
    from pages.product_page import ProductPage
    return ProductPage(driver)


@pytest.fixture
def cart_page(driver):
    """Фикстура для страницы корзины"""
    from pages.cart_page import CartPage
    return CartPage(driver)


def pytest_configure(config):
    """Конфигурация pytest"""
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Создание отчета для Allure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        try:
            if "driver" in item.fixturenames:
                driver = item.funcargs["driver"]
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
