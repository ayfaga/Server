import pygame
import sys
import time
from frontend_robot import run as robot_run  # Импорт функции run из frontend_robot.py
from frontend_data import run as data_run  # Импорт функции run из frontend_dannie.py
from frontend_camers import run as camers_run
from frontend_zakaz import run as zakaz_run
from talk.send_txt import send_file

def read_robot_count(file_path):
    """
    Считывает количество роботов из файла.
    Возвращает целое число.
    """
    try:
        with open(file_path, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        print(f"Ошибка: файл {file_path} не найден или содержит некорректные данные!")
        return 0

def load_charge_images(robot_count_file):
    """
    Загружает изображения заряда и уменьшает их в 5 раз.
    Возвращает словарь с ключами '1', '2', '3' и значениями Pygame Surface.
    """
    images = {}
    try:
        # Загружаем изображения
        images["1"] = pygame.image.load("./front/low_charge.png")
        images["2"] = pygame.image.load("./front/medium_charge.png")
        images["3"] = pygame.image.load("./front/full_charge.png")
        images["4"] = pygame.image.load("./front/no_charge.png")
        
        # Уменьшаем изображения в 5 раз
        if read_robot_count(robot_count_file) == 1 or read_robot_count(robot_count_file) == 2:
            scale = 4
        elif read_robot_count(robot_count_file) == 3 or read_robot_count(robot_count_file) == 4:
            scale = 6
        elif read_robot_count(robot_count_file) == 5 or read_robot_count(robot_count_file) == 6:
            scale = 9
        elif read_robot_count(robot_count_file) == 7 or read_robot_count(robot_count_file) == 8:
            scale = 12
        else:
            scale = 15
        for key in images:
            original_size = images[key].get_size()
            new_size = (original_size[0] // scale, original_size[1] // scale)
            images[key] = pygame.transform.scale(images[key], new_size)
    
    except pygame.error as e:
        print(f"Ошибка загрузки изображений заряда: {e}")
        pygame.quit()
        sys.exit()
    
    return images

def draw_text_wrapped(screen, text, font, color, rect, line_spacing=5):
    """
    Рисует текст с переносом внутри указанного прямоугольника.
    :param screen: Surface экрана для рисования
    :param text: Текст для вывода
    :param font: Шрифт текста
    :param color: Цвет текста
    :param rect: pygame.Rect, в котором нужно разместить текст
    :param line_spacing: Межстрочный интервал
    """
    words = text.split(" ")  # Разбиваем текст на слова
    lines = []  # Хранение строк текста
    current_line = ""  # Текущая строка

    # Формируем строки, чтобы текст помещался по ширине прямоугольника
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= rect.width:  # Проверяем, помещается ли строка
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:  # Добавляем оставшуюся строку
        lines.append(current_line)

    # Рисуем текст строки за строкой
    y_offset = rect.top
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(midtop=(rect.centerx, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += font.get_height() + line_spacing  # Сдвигаем вниз на высоту строки + интервал

def draw_table(screen, robot_count, screen_width, screen_height, charge_images, robot_headers):
    """
    Рисует таблицу на экране с выравниванием текста по центру.
    """
    # Определяем размеры таблицы
    table_x = 0  # Начало таблицы у самого левого края
    table_y = 0  # Начало таблицы у самого верхнего края
    table_width = int(screen_width * 0.7)  # 70% ширины экрана
    table_height = screen_height  # Высота таблицы на весь экран
    cell_height = table_height // 4  # Высота одной строки (4 строки)
    cell_width = table_width // (robot_count + 1)  # Ширина одного столбца

    # Цвета
    table_border_color = (0, 0, 0)  # Черный
    text_color = (0, 0, 0)  # Черный
    font = pygame.font.SysFont("Times New Roman", 24)

    # Заголовки строк
    headers = ["Робот №", "Заряд", "Ошибки"]

    clickable_areas = []  # Список для отслеживания кликабельных зон (номера роботов)

    # Первая строка (заголовок с номерами роботов)
    for col in range(robot_count + 1):
        cell_x = table_x + col * cell_width
        cell_y = table_y

        # Рисуем рамку ячейки
        pygame.draw.rect(screen, table_border_color, (cell_x, cell_y, cell_width, cell_height), 2)

        # Генерируем текст: Робот № в первой колонке, номера роботов в остальных
        if col == 0:
            header_text = font.render(headers[0], True, text_color)
        else:
            header_text = font.render(f"Р{col}", True, text_color)
            # Добавляем зону клика для робота
            clickable_areas.append((col, pygame.Rect(cell_x, cell_y, cell_width, cell_height)))

        text_rect = header_text.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
        screen.blit(header_text, text_rect)

    # Остальные строки (Заряд, Ошибки, Логи)
    for row in range(1, 3):  # 1 - "Заряд", 2 - "Ошибки", 3 - "Логи"
        for col in range(robot_count + 1):  # Количество столбцов = числу роботов
            cell_x = table_x + col * cell_width
            cell_y = table_y + row * cell_height

            # Рисуем рамку ячейки
            pygame.draw.rect(screen, table_border_color, (cell_x, cell_y, cell_width, cell_height), 2)

            # Генерируем текст: Название строки в первой колонке, пустота в остальных
            if col == 0:
                row_text = font.render(headers[row], True, text_color)
                text_rect = row_text.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
                screen.blit(row_text, text_rect)
            elif row == 1:  # Строка "Заряд"
                try:
                    with open(f"./variable_txt/robot{col}/charge.txt", "r") as f:
                        charge_level = f.read().strip()
                        if charge_level != '1' and charge_level != '2' and charge_level != '3':
                            charge_level = '4'
                        if charge_level in charge_images:
                            # Рисуем изображение заряда
                            image = charge_images[charge_level]
                            image_rect = image.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
                            screen.blit(image, image_rect)
                except FileNotFoundError:
                    pass
            elif row == 2:  # Строка "Ошибки"
                try:
                    with open(f"./variable_txt/robot{col}/errors.txt", "r", encoding='utf-8') as f:
                        error_status = f.read().strip().lower()

                        # Устанавливаем текст и цвет в зависимости от состояния ошибок
                        if "нет" in error_status or "ошибок нет" in error_status:
                            error_text = font.render("НЕТ", True, (56, 87, 35))  # Цвет для "НЕТ"
                        else:
                            error_text = font.render("ДА", True, (236, 28, 36))  # Цвет для "ДА"

                        # Центрируем текст в ячейке
                        text_rect = error_text.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
                        screen.blit(error_text, text_rect)

                except FileNotFoundError:
                    # Если файл ошибок не найден, отображаем "НЕТ" (с цветом по умолчанию)
                    error_text = font.render("НЕТ", True, (56, 87, 35))
                    text_rect = error_text.get_rect(center=(cell_x + cell_width // 2, cell_y + cell_height // 2))
                    screen.blit(error_text, text_rect)
    
    rect_areas = [pygame.Rect(0, 0, 0, 0)]*5  # Список прямоугольников

    robot_count_file = "./variable_txt/count_robots.txt"
    #ОПЕРАЦИИ
    rect = pygame.Rect(0, 3*screen_height//4, cell_width, cell_height)
    pygame.draw.rect(screen, table_border_color, rect, 3)
    info_text = "Операции"
    row_text = font.render(info_text, True, text_color)
    text_rect = row_text.get_rect(center=(0 + cell_width//2, 3*screen_height//4 + cell_height//2))
    screen.blit(row_text, text_rect)

    #1 КНОПКА
    rect = pygame.Rect(cell_width, 3*screen_height//4, (table_width-cell_width)//2, cell_height)
    pygame.draw.rect(screen, table_border_color, rect, 3)
    if read_robot_count(robot_count_file)==1 or read_robot_count(robot_count_file)==2:
        font = pygame.font.SysFont("Times New Roman", 24)
    elif read_robot_count(robot_count_file)==3 or read_robot_count(robot_count_file)==4:
        font = pygame.font.SysFont("Times New Roman", 40)
    else:
        font = pygame.font.SysFont("Times New Roman", 50)
    info_text = "Запустить функцию"
    row_text = font.render(info_text, True, text_color)
    text_rect = row_text.get_rect(center=(cell_width + (table_width-cell_width)//4, 3*screen_height//4 + cell_height//2 - cell_height//7))
    screen.blit(row_text, text_rect)
    info_text = "сканирования паспорта"
    row_text = font.render(info_text, True, text_color)
    text_rect = row_text.get_rect(center=(cell_width + (table_width-cell_width)//4, 3*screen_height//4 + cell_height//2 + cell_height//7))
    screen.blit(row_text, text_rect)
    rect_areas[3] = (rect)

    #2 КНОПКА
    rect = pygame.Rect(cell_width + (table_width-cell_width)//2, 3*screen_height//4, (table_width-cell_width)//2, cell_height)
    pygame.draw.rect(screen, table_border_color, rect, 3)
    info_text = "Запустить функцию"
    row_text = font.render(info_text, True, text_color)
    text_rect = row_text.get_rect(center=(cell_width + 3*(table_width-cell_width)//4, 3*screen_height//4 + cell_height//2 - cell_height//7))
    screen.blit(row_text, text_rect)
    info_text = "работы внутри поезда"
    row_text = font.render(info_text, True, text_color)
    text_rect = row_text.get_rect(center=(cell_width + 3*(table_width-cell_width)//4, 3*screen_height//4 + cell_height//2 + cell_height//7))
    screen.blit(row_text, text_rect)
    rect_areas[4] = rect

    # Рисуем три прямоугольника в правой части
    rect_width = screen_width - table_width  # Ширина правой области
    rect_height = screen_height // 3  # Высота каждого прямоугольника
    
    for i in range(3):
        rect = pygame.Rect(table_width, i * rect_height, rect_width, rect_height)
        pygame.draw.rect(screen, table_border_color, rect, 3)
        rect_areas[i] = (rect)
    
    rect_areas2 = []  # Список прямоугольников
    for i in range(3):
        if i == 0:
            vremenno = screen_height // 32
        elif i == 1:
            vremenno = screen_height // 8
        else:
            vremenno = screen_height // 10
        rect2 = pygame.Rect(table_width, i * rect_height+vremenno, rect_width, rect_height)
        pygame.draw.rect(screen, table_border_color, rect, 3)
        rect_areas2.append(rect2)

    # Текст в верхнем прямоугольнике с переносом
    font_large = pygame.font.SysFont("Times New Roman", 44)
    info_text = "Информация о пассажирах и база данных постоянных покупателей"
    draw_text_wrapped(screen, info_text, font_large, text_color, rect_areas2[0], line_spacing=10)

    font_large = pygame.font.SysFont("Times New Roman", 44)
    info_text = "Данные с камер"
    draw_text_wrapped(screen, info_text, font_large, text_color, rect_areas2[1], line_spacing=10)

    font_large = pygame.font.SysFont("Times New Roman", 44)
    info_text = "Информация о заказах пассажиров"
    draw_text_wrapped(screen, info_text, font_large, text_color, rect_areas2[2], line_spacing=10)

    return clickable_areas, rect_areas  # Возвращаем зоны кликов для роботов и прямоугольников

def display_error_message(screen, message, screen_width, screen_height, duration=3000):
    """
    Отображает сообщение об ошибке на экране на несколько секунд.
    :param screen: Pygame Surface для отрисовки
    :param message: Текст сообщения об ошибке
    :param screen_width: Ширина экрана
    :param screen_height: Высота экрана
    :param duration: Длительность отображения в миллисекундах (по умолчанию 3000 мс)
    """
    # Создаём шрифт
    font = pygame.font.SysFont("Times New Roman", 36)
    text_color = (255, 0, 0)  # Красный цвет для ошибки
    background_color = (221, 250, 221)  # Белый фон для сообщения
    
    # Рендер текста
    error_text = font.render(message, True, text_color, background_color)
    text_rect = error_text.get_rect(center=(screen_width // 2, screen_height // 2))
    
    # Отображаем сообщение
    screen.blit(error_text, text_rect)
    pygame.display.flip()
    
    # Ждём указанное время
    pygame.time.delay(duration)


def main():
    # Инициализация Pygame
    pygame.init()
    
    # Определяем размеры экрана
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    
    # Создаем окно на полный экран
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Российские Железные Дороги - сервер")
    
    # Цвет заднего фона (221, 250, 221)
    background_color = (221, 250, 221)
    
    # Путь к файлу с количеством роботов
    robot_count_file = "./variable_txt/count_robots.txt"
    
    # Читаем количество роботов
    robot_count = read_robot_count(robot_count_file)
    
    # Если роботов нет, выводим сообщение и завершаем работу
    if robot_count <= 0:
        display_error_message(screen, "Нет роботов для отображения!", screen_width, screen_height, duration=3000)
        pygame.quit()
        sys.exit()
    
    # Загружаем изображения заряда
    charge_images = load_charge_images(robot_count_file)

    # Основной цикл
    running = True
    while running:
        with open('./talk/received.txt', 'r', encoding='utf-8') as f:
            a=f.readline()
            if "WAIT_ADMIN" in a:
                display_error_message(screen, f'Подойдите к роботу! Вас ожидают', screen_width, screen_height, duration=2000)
                #display_error_message(screen, f'Пароль - {a.split()[1]}' screen_width, screen_height, duration=2000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = event.pos
                # Проверяем нажатие по роботу
                for robot_id, rect in clickable_areas:
                    if rect.collidepoint(mouse_pos):
                        robot_run(robot_id)
                # Проверяем нажатие на верхний прямоугольник
                if rect_areas[0].collidepoint(mouse_pos):
                    data_run()
                if rect_areas[1].collidepoint(mouse_pos):
                    camers_run()
                if rect_areas[2].collidepoint(mouse_pos):
                    zakaz_run()
                if rect_areas[3].collidepoint(mouse_pos):
                    with open('./talk/send.txt', 'w', encoding='utf-8') as f:
                        f.write('1')
                    for i in range(1, read_robot_count(robot_count_file) + 1):
                        vrem = send_file('./talk/send.txt', i)
                        if vrem == "NO_CONNECT":
                            display_error_message(screen, f'Отсутствует подключение к роботу {i}!', screen_width, screen_height, duration=2000)
                            display_error_message(screen, f'Проверьте корректность URL в файле URL_robot{i} или работоспособность робота', screen_width, screen_height, duration=2000)
                            continue
                        time.sleep(1)
                        with open('./talk/received.txt', 'r', encoding='utf-8') as f:
                            a=f.readline()
                            if a == 'NO_CSV':
                                display_error_message(screen, f'Отсутствует файл info_pass.csv на роботе {i}!', screen_width, screen_height, duration=2000)
                                display_error_message(screen, f'Добавьте его через блок "информация о маршруте"', screen_width, screen_height, duration=2000)
                                open("./talk/received.txt",'w').close()
                            else:
                                display_error_message(screen, 'Отправлено!', screen_width, screen_height, duration=1000)
                if rect_areas[4].collidepoint(mouse_pos):
                    with open('./talk/send.txt', 'w', encoding='utf-8') as f:
                        f.write('2')
                    for i in range(1, read_robot_count(robot_count_file) + 1):
                        vrem = send_file('./talk/send.txt', i)
                        if vrem == "NO_CONNECT":
                            display_error_message(screen, f'Отсутствует подключение к роботу {i}!', screen_width, screen_height, duration=2000)
                            display_error_message(screen, f'Проверьте корректность URL в файле URL_robot{i} или работоспособность робота', screen_width, screen_height, duration=2000)
                            continue
                        time.sleep(1)
                        with open('./talk/received.txt', 'r', encoding='utf-8') as f:
                            if f.readline() == 'NO_CSV':
                                display_error_message(screen, f'Отсутствует файл info_pass.csv на роботе {i}!', screen_width, screen_height, duration=2000)
                                display_error_message(screen, f'Добавьте его через блок "информация о маршруте"', screen_width, screen_height, duration=2000)
                                open("./talk/received.txt",'w').close()
                            else:
                                display_error_message(screen, 'Отправлено!', screen_width, screen_height, duration=1000)

        screen.fill(background_color)
        clickable_areas, rect_areas = draw_table(screen, robot_count, screen_width, screen_height, charge_images, [])
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
