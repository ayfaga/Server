import pygame
import sys
import os
import time
import subprocess

python_executable = sys.executable

def read_orders(file_path):
    """
    Читает данные из файла zakaz.txt и форматирует их в список строк заказа.
    Возвращает список заказов для отображения в таблице.
    """
    orders = []
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            lines = file.readlines()
            order_num = 1  # Порядковый номер заказа
            for line in lines:
                parts = line.strip().split()
                if len(parts) < 4:
                    continue  # Пропускаем некорректные строки

                # Разбираем строку заказа
                vagon = parts[0]
                mesto = parts[1]
                product_data = " ".join(parts[2:-1])  # Продукты с количеством
                status = parts[-1]

                # Если статус "ЗАВЕРШЕНО", пропускаем заказ
                if status == "ЗАВЕРШЕНО":
                    continue

                # Парсим продукты и их количество
                products = product_data.strip("()").split(", ")
                for product in products:
                    name, qty = product.split(" x")
                    orders.append({
                        "num": order_num,
                        "vagon": vagon.replace(',', ''),
                        "mesto": mesto.replace(',', ''),
                        "product": name.strip(),
                        "quantity": qty.strip(),
                        "status": status
                    })
                    order_num += 1
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!")
        sys.exit()

    return orders


def run():
    # Инициализация Pygame
    pygame.init()

    # Получаем размеры экрана
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h

    # Создаем окно с заданным разрешением
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Российские Железные Дороги - заказы")

    # Задаём RGB цвет для фона
    background_color = (221, 250, 221)

    # Рассчитываем ширины колонок
    col_widths = [
        screen_width // 16,
        2 * screen_width // 16,
        2 * screen_width // 16,
        5 * screen_width // 16,
        2 * screen_width // 16,
        4 * screen_width // 16,
    ]

    # Координата X для каждой колонки
    col_positions = [sum(col_widths[:i]) for i in range(len(col_widths))]

    # Рассчитываем высоту каждой строки
    row_height = screen_height // 14

    # Шрифт для текста
    font = pygame.font.SysFont("Times New Roman", 24)

    # Названия колонок
    headers = ["Номер", "Вагон", "Место", "Продукт", "Количество", "Статус"]

    # Путь к файлу
    file_path = "./variable_txt/zakaz.txt"

    # Время последнего изменения файла
    last_mtime = 0

    # Загружаем заказы из файла
    orders = read_orders(file_path)

    # Основной цикл
    running = True
    while running:
        # Проверяем изменения в файле каждые 2 секунды
        current_mtime = os.path.getmtime(file_path)
        if current_mtime != last_mtime:
            last_mtime = current_mtime
            orders = read_orders(file_path)  # Перезагружаем данные из файла

        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Получаем координаты мыши при клике
                mouse_x, mouse_y = event.pos
                # Если нажали на кнопку "Вернуться назад"
                if button_exit_x <= mouse_x <= button_exit_x + button_exit_width and button_exit_y <= mouse_y <= button_exit_y + button_exit_height:
                    pygame.quit()  # Корректно завершаем Pygame
                    subprocess.Popen([python_executable, "frontend_server.py"])
                    sys.exit()  # Завершаем текущий процесс

        # Заполняем экран заданным цветом
        screen.fill(background_color)

        # Рисуем строки и колонки
        for row in range(14):  # Всего 14 строк
            row_y = row * row_height

            # Фон строки
            row_color = (230, 230, 230) if row % 2 == 0 else (255, 255, 255)
            pygame.draw.rect(screen, row_color, (0, row_y, screen_width, row_height))

            # Рисуем рамки ячеек
            for col in range(6):  # Всего 6 колонок
                col_x = col_positions[col]
                col_width = col_widths[col]
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),  # Цвет рамки (чёрный)
                    pygame.Rect(col_x, row_y, col_width, row_height),
                    1  # Толщина рамки
                )

                # Если это первая строка, добавляем заголовки
                if row == 0:
                    header_text = headers[col]
                    text_surface = font.render(header_text, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=(col_x + col_width // 2, row_y + row_height // 2))
                    screen.blit(text_surface, text_rect)
                else:
                    # Заполняем строки данными заказов
                    order_index = row - 1  # Учитываем, что первая строка — это заголовок
                    if order_index < len(orders):
                        order = orders[order_index]
                        cell_values = [
                            str(order["num"]),
                            order["vagon"],
                            order["mesto"],
                            order["product"],
                            order["quantity"],
                            order["status"]
                        ]
                        # Добавляем данные в ячейки строки
                        cell_text = cell_values[col]
                        text_surface = font.render(cell_text, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=(col_x + col_width // 2, row_y + row_height // 2))
                        screen.blit(text_surface, text_rect)

        button_exit_text_color = (255, 255, 255) 
        button_exit_color = (56, 87, 35)  # Зеленый цвет
        button_exit_width = screen_width//6
        button_exit_height = 4*screen_height//36
        button_exit_x = screen_width - button_exit_width - screen_width//12
        button_exit_y = screen_height - button_exit_height - screen_height//36
        button_exit_font = pygame.font.SysFont("Times New Roman", 30, bold=True)
        pygame.draw.rect(screen, button_exit_color, (button_exit_x, button_exit_y, button_exit_width, button_exit_height))
        button_exit_text_surface = button_exit_font.render("Вернуться назад", True, button_exit_text_color)
        button_exit_text_rect = button_exit_text_surface.get_rect(center=(button_exit_x + button_exit_width // 2, button_exit_y + button_exit_height // 2))
        screen.blit(button_exit_text_surface, button_exit_text_rect)

        # Обновляем экран
        pygame.display.flip()

        # Задержка на 2 секунды
        time.sleep(2)

    # Корректное завершение работы
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run()
