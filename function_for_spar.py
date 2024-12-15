from pkgutil import resolve_name

from playwright.sync_api import sync_playwright

def initialize_browser():
    """Инициализация браузера и создание новой страницы."""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    return playwright, browser, page

def search_product(page, product_name):
    """Поиск продукта по имени."""
    search_input_selector = '.header-control__text.d-none.d-md-block'  # Селектор для поля ввода
    page.goto('https://myspar.ru/')
    #page.wait_for_selector(search_input_selector, timeout=60000)
    page.click(search_input_selector)
    #page.wait_for_selector('#input-smartsearch')
    page.fill('#input-smartsearch', product_name)
    page.wait_for_selector('.smartsearch__result')  # Ожидание результатов
    page.click('a[data-category-name="Овощи"]')

def close_browser(playwright, browser):
    """Закрытие браузера."""
    browser.close()
    playwright.stop()

def get_number_of_pages(page):
    """Получение количества страниц в пагинации."""
    pagination_selector = '.smartsearch__pagination li[data-page]'  # Убедитесь, что селектор правильный
    page.wait_for_selector(pagination_selector)  # Ожидание появления элементов пагинации
    pages = page.query_selector_all(pagination_selector)  # Получение всех элементов пагинации

    # Фильтруем элементы, чтобы убедиться, что мы считаем только страницы
    page_numbers = [p for p in pages if p.inner_text().isdigit()]
    return len(page_numbers)  # Возвращаем количество страниц

def navigate_to_page(page, page_number):
    """Навигация к указанной странице."""
    page.click(f'li[data-page="{page_number}"]')  # Клик по нужной странице
    # Ожидание появления первого продукта на новой странице
    page.wait_for_selector('.smartsearch__product', timeout=5000)  # Установите таймаут по необходимости


def extract(page):
    """Извлечение названий и цен продуктов из результатов поиска."""
    products = page.query_selector_all('.smartsearch__product')  # Получаем все продукты
    product_data = []
    unique_names = set()  # Множество для хранения уникальных названий

    # Извлекаем наименование и цену для каждого продукта
    for product in products:
        # Извлекаем наименование
        name_element = product.query_selector('.smartsearch__product-info .smartsearch__product-name')
        price_element = product.query_selector('.smartsearch__product-info-bottom .smartsearch__product-price')

        # Получаем текст наименования и цены
        res_name = name_element.inner_text().strip() if name_element else 'Не указано'
        res_price = price_element.inner_text().strip() if price_element else 'Не указано'

        # Проверяем, уникально ли название
        if res_name not in unique_names:
            unique_names.add(res_name)  # Добавляем название в множество
            # Добавляем данные в список в виде словаря
            product_data.append({
                'name': res_name,
                'price': res_price
            })

    print(f"Найдено уникальных продуктов на странице: {len(product_data)}")  # Отладочное сообщение
    return product_data


