import pygame
import cv2
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

python_executable = sys.executable

def read_camera_urls(file_path):
    """
    Читает IP камер из файла и возвращает список URL.
    """
    try:
        with open(file_path, "r") as file:
            urls = [f"http://{line.strip()}/video" for line in file.readlines()]
        return urls
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!")
        sys.exit()


def divide_screen(n, screen_width, screen_height):
    """
    Рассчитывает размещение n прямоугольников с пропорциями 16:9 на экране.
    """
    aspect_ratio = 16 / 9
    rows = cols = 1

    while rows * cols < n:
        if (screen_width / cols) / (screen_height / rows) > aspect_ratio:
            rows += 1
        else:
            cols += 1

    rect_width = screen_width // cols
    rect_height = int(rect_width / aspect_ratio)

    if rect_height * rows > screen_height:
        rect_height = screen_height // rows
        rect_width = int(rect_height * aspect_ratio)

    return rows, cols, rect_width, rect_height


def check_camera_connection(url):
    """
    Проверяет подключение к камере.
    Возвращает True, если камера доступна, иначе False.
    """
    cap = cv2.VideoCapture(url)
    is_connected = cap.isOpened()
    cap.release()
    return is_connected


def draw_video_rectangles(screen, rows, cols, rect_width, rect_height, camera_states, font):
    """
    Рисует прямоугольники для камер с подписями и состоянием.
    """
    for i, state in enumerate(camera_states):
        row = i // cols
        col = i % cols

        x = col * rect_width
        y = row * rect_height

        # Рисуем рамку прямоугольника
        pygame.draw.rect(screen, (0, 0, 0), (x, y, rect_width, rect_height), 5)

        # Если камера недоступна, вывести сообщение об ошибке
        if state == "error":
            error_message = f"{i + 1}"
            error_font = pygame.font.SysFont("Arial", 25)
            text_surface = error_font.render(error_message, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x + rect_width // 2, y + rect_height // 2))
            screen.blit(text_surface, text_rect)


def display_camera_video(screen, rect, url):
    """
    Отображает видео с камеры в указанном прямоугольнике.
    """
    cap = cv2.VideoCapture(url)
    success, frame = cap.read()
    if success:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (rect[2], rect[3]))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        screen.blit(frame_surface, (rect[0], rect[1]))
    cap.release()


def run():
    pygame.init()

    # Загружаем список камер
    camera_urls = read_camera_urls("./variable_txt/camers.txt")
    num_cameras = len(camera_urls)

    # Получаем размеры экрана
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h

    # Рассчитываем расположение прямоугольников для камер
    rows, cols, rect_width, rect_height = divide_screen(num_cameras, screen_width, screen_height)

    # Создаем окно
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Российские Железные Дороги - камеры")
    background_color = (221, 250, 221)

    font = pygame.font.SysFont("Times New Roman", 20)
    clock = pygame.time.Clock()

    # Параметры для камер
    camera_states = ["checking"] * num_cameras  # Состояние каждой камеры (checking, error, success)
    camera_caps = [None] * num_cameras  # Для хранения объектов VideoCapture

    def initialize_camera(i, url):
        """
        Проверяет камеру и возвращает её состояние (success или error).
        """
        if check_camera_connection(url):
            return "success", cv2.VideoCapture(url)
        return "error", None

    # Параллельно проверяем камеры
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(initialize_camera, i, url) for i, url in enumerate(camera_urls)]
        for future in as_completed(futures):
            i, (state, cap) = futures.index(future), future.result()
            camera_states[i] = state
            camera_caps[i] = cap
    
    button_exit_text_color = (255, 255, 255) 
    button_exit_color = (56, 87, 35)  # Зеленый цвет
    button_exit_width = screen_width//6
    button_exit_height = 4*screen_height//36
    button_exit_x = screen_width - button_exit_width - screen_width//12
    button_exit_y = screen_height - button_exit_height - screen_height//36
    button_exit_font = pygame.font.SysFont("Times New Roman", 30, bold=True)
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

        # Заполняем фон
        screen.fill(background_color)

        # Рисуем рамки и состояния
        draw_video_rectangles(screen, rows, cols, rect_width, rect_height, camera_states, font)
        pygame.draw.rect(screen, button_exit_color, (button_exit_x, button_exit_y, button_exit_width, button_exit_height))
        button_exit_text_surface = button_exit_font.render("Вернуться назад", True, button_exit_text_color)
        button_exit_text_rect = button_exit_text_surface.get_rect(center=(button_exit_x + button_exit_width // 2, button_exit_y + button_exit_height // 2))
        screen.blit(button_exit_text_surface, button_exit_text_rect)

        # Отображаем видео для доступных камер
        for i, state in enumerate(camera_states):
            if state == "success":
                row = i // cols
                col = i % cols
                rect = (col * rect_width, row * rect_height, rect_width, rect_height)
                display_camera_video(screen, rect, camera_urls[i])

        # Рисуем кнопку "Вернуться назад" в каждом кадре

        pygame.draw.rect(screen, button_exit_color, (button_exit_x, button_exit_y, button_exit_width, button_exit_height))
        button_exit_text_surface = button_exit_font.render("Вернуться назад", True, button_exit_text_color)
        button_exit_text_rect = button_exit_text_surface.get_rect(center=(button_exit_x + button_exit_width // 2, button_exit_y + button_exit_height // 2))
        screen.blit(button_exit_text_surface, button_exit_text_rect)


        pygame.display.flip()
        clock.tick(20)

        # Заполняем фон
        screen.fill(background_color)

        # Рисуем рамки и состояния
        draw_video_rectangles(screen, rows, cols, rect_width, rect_height, camera_states, font)

        # Отображаем видео для доступных камер
        for i, state in enumerate(camera_states):
            if state == "success":
                row = i // cols
                col = i % cols
                rect = (col * rect_width, row * rect_height, rect_width, rect_height)
                display_camera_video(screen, rect, camera_urls[i])

        pygame.display.flip()
        clock.tick(20)

    # Освобождаем ресурсы
    for cap in camera_caps:
        if cap:
            cap.release()

    pygame.quit()
    sys.exit()