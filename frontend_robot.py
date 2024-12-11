import pygame
import sys
import subprocess  # Для запуска frontend_server.py
import sys

python_executable = sys.executable


def read_file(robot_id, file_path, default_value=""):
    """
    Функция для безопасного чтения файла.
    Если файл не найден, возвращается значение по умолчанию.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines() if f"./variable_txt/robot{robot_id}/logs.txt" in file_path else f.read().strip()
    except FileNotFoundError:
        return default_value if f"./variable_txt/robot{robot_id}/logs.txt" not in file_path else [f"Файл {file_path} не найден!"]

def run(robot_id):
    # Инициализация Pygame
    pygame.init()
    
    # Определяем размеры экрана
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    
    # Создаем окно на полный экран
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Российские Железные Дороги - роботы")
    
    # Толщина линий
    line_thickness = 5  # Можно менять значение
    
    # Загружаем фон
    try:
        background = pygame.image.load("./front/fon.png")
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except pygame.error as e:
        print(f"Ошибка загрузки фона: {e}")
        pygame.quit()
        sys.exit()
    
    # Файлы изображений и текста
    charge_images = {
        "4": "./front/no_charge.png",
        "3": "./front/full_charge.png",
        "2": "./front/medium_charge.png",
        "1": "./front/low_charge.png"
    }
    charge_txt_path = f"./variable_txt/robot{robot_id}/charge.txt"
    errors_txt_path = f"./variable_txt/robot{robot_id}/errors.txt"
    logs_txt_path = f"./variable_txt/robot{robot_id}/logs.txt"

    # Шрифт для отображения логов
    logs_font = pygame.font.SysFont("Times New Roman", 14)
    
    # Таймер для управления обновлением
    clock = pygame.time.Clock()

    # Координаты и размеры кнопки "Вернуться назад"
    button_width = 200
    button_height = 50
    button_x = 15
    button_y = screen_height - button_height - 15
    button_color = (56, 87, 35)  # Зеленый цвет кнопки
    button_text_color = (255, 255, 255)  # Белый текст
    
    button_font = pygame.font.SysFont("Times New Roman", 24, bold=True)

    # Основной игровой цикл
    running = True
    while running:
        # Проверяем события (например, закрытие окна)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Обработка кликов мыши
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Левая кнопка мыши
                mouse_x, mouse_y = event.pos
                # Если нажали на кнопку "Вернуться назад"
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    pygame.quit()  # Корректно завершаем Pygame
                    subprocess.Popen([python_executable, "frontend_server.py"])
                    sys.exit()  # Завершаем текущий процесс

        # Чтение данных из файлов каждые 0,4 секунды
        charge_state = read_file(robot_id, charge_txt_path, "1")  # Заряд
        error_message = read_file(robot_id, errors_txt_path, "Файл не найден")  # Ошибки
        logs = read_file(robot_id, logs_txt_path, ["Файл logs.txt не найден!"])  # Логи

        # Загружаем изображение заряда
        charge_image = None
        if charge_state in charge_images:
            try:
                charge_image = pygame.image.load(charge_images[charge_state])
                # Пропорциональное масштабирование изображения
                square_width = 3 * screen_width // 8
                square_height = screen_height // 3
                max_width = square_width - 30
                max_height = square_height - 30
                image_width, image_height = charge_image.get_width(), charge_image.get_height()

                scale_factor = min(max_width / image_width, max_height / image_height)
                new_width = int(image_width * scale_factor)
                new_height = int(image_height * scale_factor)

                charge_image = pygame.transform.scale(charge_image, (new_width, new_height))
            except pygame.error as e:
                print(f"Ошибка загрузки изображения заряда: {e}")
                pygame.quit()
                sys.exit()
        else:
            print(f"Некорректное значение в {charge_txt_path}!")

        # Отображение на экране
        # Отображаем фон
        screen.blit(background, (0, 0))

        # Заполнение правого нижнего квадрата зеленым цветом
        logs_x_start = 3 * screen_width // 8 + 15  # Координата X начала правого нижнего квадрата
        logs_y_start = screen_height // 3 + 15  # Координата Y начала правого нижнего квадрата
        logs_width = screen_width - logs_x_start - 15  # Ширина правого нижнего квадрата
        logs_height = screen_height - logs_y_start - 15  # Высота правого нижнего квадрата
        pygame.draw.rect(screen, (221, 250, 221), (logs_x_start - 15, logs_y_start - 15, logs_width + 30, logs_height + 30))

        # Рисуем линии
        pygame.draw.line(screen, (0, 0, 0), (3 * screen_width // 8, 0), (3 * screen_width // 8, screen_height), line_thickness)
        pygame.draw.line(screen, (0, 0, 0), (0, screen_height // 3), (screen_width, screen_height // 3), line_thickness)
        
        # Рисуем изображение заряда в левом верхнем квадрате
        if charge_image:
            charge_image_x = 15
            charge_image_y = 15
            screen.blit(charge_image, (charge_image_x, charge_image_y))
        
        # Вывод текста в правом верхнем квадрате
        if error_message.lower() == "ошибок нет" or error_message.lower() == "нет":
            font = pygame.font.SysFont("Times New Roman", 180)
            text_color = (56, 87, 35)  # Зелёный
            message = "Ошибок нет"
        else:
            font = pygame.font.SysFont("Times New Roman", 75)
            text_color = (236, 28, 36)  # Красный
            message = f"Ошибка {error_message}"

        text_surface = font.render(message, True, text_color)
        text_x = 3 * screen_width // 8 + 15  # Отступ от левой границы правого верхнего квадрата
        text_y = 15  # Отступ сверху в правом верхнем квадрате
        screen.blit(text_surface, (text_x, text_y))
        
        # Отображаем строки логов в правом нижнем квадрате
        line_height = 20  # Расстояние между строками
        max_lines = logs_height // line_height  # Максимальное количество строк
        visible_logs = logs[-max_lines:]  # Берём только последние строки, чтобы они помещались
        
        for i, log in enumerate(visible_logs):
            log_text = logs_font.render(log.strip(), True, (0, 0, 0))  # Чёрный цвет текста
            screen.blit(log_text, (logs_x_start, logs_y_start + i * line_height))

        # Рисуем кнопку "Вернуться назад"
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        button_text_surface = button_font.render("Вернуться назад", True, button_text_color)
        button_text_rect = button_text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text_surface, button_text_rect)

        # Обновляем экран
        pygame.display.flip()

        # Ждём 0,4 секунды
        clock.tick(6.25)  # 2.5 FPS = 0.4 секунды на кадр
    
    # Завершение работы Pygame
    pygame.quit()
