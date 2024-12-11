import pygame
import sys
import subprocess
from tkinter import Tk, filedialog
import shutil
import os
from talk.send_csv import send_csv

python_executable = sys.executable
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

def draw_text(surface, text, font, color, x, y):
    """
    Рисует текст на экране по указанным координатам.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


def draw_button(surface, text, font, color, x, y, width, height):
    """
    Рисует кнопку с текстом на экране.
    """
    pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 2)  # Рисуем рамку кнопки
    draw_text(surface, text, font, color, x + 10, y + 10)  # Отступ для текста внутри кнопки


# Глобальные переменные для отображения сообщений
message_text = ""
message_color = (0, 0, 0)
message_time = 0


# Функции для кнопок
def recieve_info():
    """
    Открывает окно выбора файла и выводит путь к выбранному файлу.
    """
    global message_text, message_color, message_time

    # Инициализация Tkinter
    root = Tk()
    root.withdraw()  # Скрыть основное окно Tkinter

    # Открыть диалог выбора файла
    file_path = filedialog.askopenfilename(title="Выберите .csv файл для получения информации", filetypes=[(".csv файл", "*.csv")])

    # Выводим путь к файлу (или сообщение, если файл не выбран)
    if file_path:
        try:
            # Копируем файл
            shutil.copy(file_path, "./info_pass.csv")
            message_text = "Успешно! Данные считаны!"  # Сообщение об успехе
            message_color = (56, 87, 35)  # Зеленый цвет
        except Exception as e:
            message_text = f"Ошибка: {e}"  # Сообщение об ошибке
            message_color = (236, 28, 36)  # Красный цвет
    else:
        message_text = "Файл не выбран!"
        message_color = (236, 28, 36)  # Красный цвет

    # Устанавливаем время, чтобы удалить сообщение через 3 секунды
    message_time = pygame.time.get_ticks()

    # Уничтожить окно Tkinter
    root.destroy()


def send_info():
    """
    Открывает окно выбора папки и выводит путь к выбранной папке.
    """
    global message_text, message_color, message_time

    # Инициализация Tkinter
    root = Tk()
    root.withdraw()  # Скрыть основное окно Tkinter

    # Открыть диалог выбора папки
    folder_path = filedialog.askdirectory(title="Выберите место для установки")

    if folder_path:
        try:
            # Копируем файл
            shutil.copy("./bdpokyp.csv", folder_path)
            message_text = "Успешно! Данные считаны!"  # Сообщение об успехе
            message_color = (56, 87, 35)  # Зеленый цвет
        except Exception as e:
            message_text = f"Ошибка: {e}"  # Сообщение об ошибке
            message_color = (236, 28, 36)  # Красный цвет
    else:
        message_text = "Файл не выбран!"
        message_color = (236, 28, 36)  # Красный цвет

    # Выводим путь к выбранной папке (или сообщение, если папка не выбрана)
    if folder_path:
        message_text = f"Успешно! Данные перенесены!"  # Путь выбранной папки
        message_color = (56, 87, 35)  # Зеленый цвет
    else:
        message_text = "Папка не выбрана!"
        message_color = (236, 28, 36)  # Красный цвет

    # Устанавливаем время, чтобы удалить сообщение через 3 секунды
    message_time = pygame.time.get_ticks()

    # Уничтожить окно Tkinter
    root.destroy()


def send_all_robots():
    global message_text, message_color, message_time
    robot_count_file = "./variable_txt/count_robots.txt"
    for i in range(1, read_robot_count(robot_count_file) + 1):
        if os.path.isfile('./info_pass.csv'):
            vrem = send_csv('./info_pass.csv', i)
            if vrem ==  "NO_CONNECT":
                message_text = f'Нет соединения с роботом {i}'
                message_color = (236, 28, 36)  # Красный цвет
            else:
                message_text = f'Отправлено!'
                message_color = (236, 28, 36)  # Зеленый цвет
        else:
            message_text = 'Отсутствует файл info_pass.csv'
            message_color = (236, 28, 36)  # Красный цвет
    message_time = pygame.time.get_ticks()


def open_database():
    global message_text, message_color, message_time
    try:
        # Проверяем наличие файла 
        if os.path.exists("bdpokyp.csv"):
            # Открываем файл в Excel
            os.startfile("bdpokyp.csv")
        else:
            message_text = "Ошибка! База данных не обнаружена!"  # Сообщение об успехе
            message_color = (236, 28, 36)  # Зеленый цвет
    except Exception as e:
        message_text = "Ошибка "+ str(e)
        message_color = (236, 28, 36)  # Красный цвет

    message_time = pygame.time.get_ticks()


def run():
    # Указываем, что переменные глобальные
    global message_text, message_color, message_time

    # Инициализация Pygame
    pygame.init()

    # Получаем размеры экрана
    screen_info = pygame.display.Info()
    global screen_width
    global screen_height
    screen_width, screen_height = screen_info.current_w, screen_info.current_h

    # Создаем окно на полный экран
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Российские Железные Дороги - данные")

    # Цвет фона
    background_color = (221, 250, 221)

    # Толщина линии и цвет
    line_color = (38, 38, 38)  # Черный цвет
    line_thickness = 5

    # Шрифт для текста и кнопок
    font = pygame.font.SysFont("Times New Roman", 40)
    button_font = pygame.font.SysFont("Arial", 20)

    # Размеры кнопок
    button_width = screen_width // 4
    button_height = 40

    # Кнопки (для упрощения, создадим список с координатами, размерами и функциями)
    buttons = [
        {"text": "Получить информацию с USB-накопителя", "x": screen_width // 48, "y": screen_height // 5, "width": button_width, "height": button_height, "action": recieve_info},
        {"text": "Перенести информацию на всех роботов", "x": screen_width // 48, "y": screen_height // 5 + button_height + screen_height // 36, "width": button_width, "height": button_height, "action": send_all_robots},
        {"text": "Перенести данные на USB-накопитель", "x": screen_width // 2 + screen_width // 48, "y": screen_height // 5, "width": button_width, "height": button_height, "action": send_info},
        {"text": "Показать базу данных", "x": screen_width // 2 + screen_width // 48, "y": screen_height // 5 + button_height + screen_height // 36, "width": button_width, "height": button_height, "action": open_database}
    ]

    # Основной цикл приложения
    running = True
    while running:
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
                    
                # Проверяем, в какой кнопке был клик
                for button in buttons:
                    if button["x"] <= mouse_x <= button["x"] + button["width"] and button["y"] <= mouse_y <= button["y"] + button["height"]:
                        button["action"]()  # Запускаем соответствующую функцию кнопки

        # Заполняем экран цветом фона
        screen.fill(background_color)

        # Левый прямоугольник (слева от вертикальной линии)
        left_rect_width = screen_width // 2
        left_rect_height = screen_height
        pygame.draw.rect(screen, (221, 250, 221), (0, 0, left_rect_width, left_rect_height))  # Левый прямоугольник

        # Текст "Информация о пассажирах на маршруте"
        draw_text(screen, "Информация о пассажирах на маршруте", font, (0, 0, 0), screen_width // 48, screen_height // 36)

        # Кнопки в левом прямоугольнике
        for i, button in enumerate(buttons[:2]):
            draw_button(screen, button["text"], button_font, (0, 0, 0), button["x"], button["y"], button["width"], button["height"])

        # Правый прямоугольник (справа от вертикальной линии)
        right_rect_x = screen_width // 2
        pygame.draw.rect(screen, (221, 250, 221), (right_rect_x, 0, left_rect_width, left_rect_height))  # Правый прямоугольник

        # Текст "База данных постоянных покупателей"
        draw_text(screen, "База данных постоянных покупателей", font, (0, 0, 0), right_rect_x + screen_width // 48, screen_height // 36)

        # Кнопки в правом прямоугольнике
        for _, button in enumerate(buttons[2:]):
            draw_button(screen, button["text"], button_font, (0, 0, 0), button["x"], button["y"], button["width"], button["height"])

        # Рисуем вертикальную линию по центру
        pygame.draw.line(screen, line_color, (screen_width // 2, 0), (screen_width // 2, screen_height), line_thickness)

        # Нижний прямоугольник
        pygame.draw.rect(screen, (38, 38, 38), (0, screen_height-screen_height // 6, screen_width, screen_height // 6))  # Нижний прямоугольник

        button_exit_text_color = (255, 255, 255) 
        button_exit_color = (38, 38, 38)  # Зеленый цвет
        button_exit_width = screen_width//6
        button_exit_height = 4*screen_height//36
        button_exit_x = screen_width - button_exit_width - screen_width//12
        button_exit_y = screen_height - button_exit_height - screen_height//36
        button_exit_font = pygame.font.SysFont("Times New Roman", 30, bold=True)
        # Рисуем кнопку "Вернуться назад"

        # Отображение сообщения (если оно есть) в нижней части экрана
        if message_text:
            draw_text(
                screen,
                message_text,
                pygame.font.SysFont("Times New Roman", 60),
                message_color,
                screen_width // 26,
                screen_height - screen_height // 8,
            )

            # Убираем сообщение через 3 секунды
            if pygame.time.get_ticks() - message_time > 3000:
                message_text = ""

        # Обновляем экран
        pygame.draw.rect(screen, button_exit_color, (button_exit_x, button_exit_y, button_exit_width, button_exit_height))
        button_exit_text_surface = button_exit_font.render("Вернуться назад", True, button_exit_text_color)
        button_exit_text_rect = button_exit_text_surface.get_rect(center=(button_exit_x + button_exit_width // 2, button_exit_y + button_exit_height // 2))
        screen.blit(button_exit_text_surface, button_exit_text_rect)
        pygame.display.flip()

    # Завершаем работу Pygame
    pygame.quit()
    sys.exit()

