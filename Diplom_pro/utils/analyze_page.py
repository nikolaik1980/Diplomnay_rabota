"""Утилита для анализа структуры страницы"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def analyze_chitai_gorod():
    """Анализ структуры сайта Читай-город"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # В фоновом режиме
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        print("Открываем сайт Читай-город...")
        driver.get("https://www.chitai-gorod.ru/")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Принимаем куки
        try:
            cookie_selector = "button.cookie-policy__agree"
            cookie_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, cookie_selector))
            )
            cookie_button.click()
            # Ждем немного после клика на куки
            wait.until(lambda d: d.execute_script(
                "return document.readyState") == "complete"
            )
        except Exception:
            print("Кнопка куки не найдена")

        print("\n=== ПОИСК ПОИСКОВОЙ СТРОКИ ===")

        # Ищем все возможные поисковые строки
        search_selectors = [
            ("header-search__input", "input.header-search__input"),
            ("search-input", "input.search-input"),
            ("search field", "input[type='search']"),
            ("q field", "input[name='q']"),
            ("search text", "input[type='text'][name*='search']"),
            ("any input", "input"),
        ]

        for name, selector in search_selectors:
            try:
                # Используем явное ожидание
                elements = wait.until(
                    lambda d: d.find_elements(By.CSS_SELECTOR, selector)
                )
                if elements:
                    elements_count = len(elements)
                    print(f"\nНайдено по селектору '{name}' "
                          f"({selector}): {elements_count} элементов")
                    for i, elem in enumerate(elements[:3]):  # Покажем первые 3
                        print(f"  Элемент {i}:")
                        print(f"    type: {elem.get_attribute('type')}")
                        print(f"    name: {elem.get_attribute('name')}")
                        attr_placeholder = elem.get_attribute('placeholder')
                        print(f"    placeholder: {attr_placeholder}")
                        print(f"    class: {elem.get_attribute('class')}")
                        print(f"    id: {elem.get_attribute('id')}")
            except Exception as e:
                print(f"Ошибка при поиске {name}: {e}")

        print("\n=== КНОПКИ ПОИСКА ===")
        button_selectors = [
            ("header-search__btn", "button.header-search__btn"),
            ("search-button", "button.search-button"),
            ("submit button", "button[type='submit']"),
            ("any button near input", "button"),
        ]

        for name, selector in button_selectors:
            try:
                elements = wait.until(
                    lambda d: d.find_elements(By.CSS_SELECTOR, selector)
                )
                if elements:
                    elements_count = len(elements)
                    print(f"\nНайдено по селектору '{name}': "
                          f"{elements_count} элементов")
                    for i, elem in enumerate(elements[:3]):
                        print(f"  Кнопка {i}:")
                        print(f"    text: {elem.text}")
                        print(f"    class: {elem.get_attribute('class')}")
            except Exception:
                pass

        print("\n=== КНОПКА КОРЗИНЫ ===")
        cart_selectors = [
            ("header-cart", ".header-cart, .cart-button, .basket-button"),
            ("cart link", "[href*='cart'], [href*='basket']"),
        ]

        for name, selector in cart_selectors:
            try:
                elements = wait.until(
                    lambda d: d.find_elements(By.CSS_SELECTOR, selector)
                )
                if elements:
                    elements_count = len(elements)
                    print(f"\nНайдено по селектору '{name}': "
                          f"{elements_count} элементов")
                    for i, elem in enumerate(elements[:2]):
                        print(f"  Корзина {i}:")
                        print(f"    text: {elem.text}")
                        print(f"    href: {elem.get_attribute('href')}")
            except Exception:
                pass

        print("\n=== ПРОДУКТЫ НА ГЛАВНОЙ ===")
        product_selectors = [
            ("product-card", ".product-card, article.product-card"),
            ("book-item", ".book-item, .product-item"),
        ]

        for name, selector in product_selectors:
            try:
                elements = wait.until(
                    lambda d: d.find_elements(By.CSS_SELECTOR, selector)
                )
                if elements:
                    elements_count = len(elements)
                    print(f"\nНайдено по селектору '{name}': "
                          f"{elements_count} элементов")
                    break
            except Exception:
                pass

        # Сохраним скриншот
        driver.save_screenshot("page_analysis.png")
        print("\nСкриншот сохранен как 'page_analysis.png'")

    finally:
        driver.quit()


if __name__ == "__main__":
    analyze_chitai_gorod()
