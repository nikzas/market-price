from function_for_spar import *

def main(product_name):
    """Основная функция для выполнения поиска и извлечения результатов."""
    playwright, browser, page = initialize_browser()
    all_product_data = []
    try:
        page.goto('https://myspar.ru/')  # Переход на сайт
        search_product(page, product_name)  # Поиск на первой странице

        # Получение количества страниц
        total_pages = get_number_of_pages(page)
        print(f"Всего страниц: {total_pages}")

        for page_number in range(1, total_pages + 1):
            print(f"Извлечение данных со страницы {page_number}...")
            product_data = extract(page)  # Извлечение данных с текущей страницы
            all_product_data.extend(product_data)  # Используем extend для добавления элементов списка
            print(f"Скачана страница {page_number}... Найдено продуктов: {len(product_data)}")

            if page_number < total_pages:  # Переход на следующую страницу, если это не последняя
                navigate_to_page(page, page_number + 1)  # Переход на следующую страницу

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        close_browser(playwright, browser)
        return all_product_data  # Возвращаем все данные о продуктах

if __name__ == "__main__":
    product_name = 'помидоры'
    products = main(product_name)
    print(f"Общее количество продуктов: {len(products)}")
    print(products)