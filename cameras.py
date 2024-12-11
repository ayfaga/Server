import cv2
import time
import sys
import os
import pygame
from fight_detection import Fight_utils
from random import *

sys.stderr = open(os.devnull, 'w')

# Читаем список URL камер
with open('./variable_txt/camers.txt', 'r') as f:
    a = f.readlines()

url = [f"http://{i.strip()}/video" for i in a]

# Настройки для видео записи
video_duration = 5
frame_width = 1280
frame_height = 720
fps = 20
W, H = 16, 9


def analyze_video(video_path, camera_index, i):
    """
    Анализирует видео на наличие драки.
    Если драка обнаружена, запускает Pygame окно для отображения видео и кнопок.
    """
    result = Fight_utils.fightDetection(video_path, 20, 1, './', True)
    if "fight" in result:
        print(f"Драка обнаружена на видео с камеры {camera_index}")
        show_video_pygame(i, camera_index)


def show_video_pygame(video_path, camera_index):
    """
    Открывает видео с камеры в Pygame, добавляет фон и кнопки.
    """
       # Инициализация Pygame
    pygame.init()

    # Получаем размеры экрана
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h

    # Устанавливаем окно на передний план
    pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

    # Создаем окно с заданным разрешением
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Российские Железные Дороги - девиантное поведение")

    # Цвета
    background_color = (221, 250, 221)
    button_color = (200, 200, 200)
    button_hover_color = (150, 150, 150)
    text_color = (0, 0, 0)

    # Шрифт
    font = pygame.font.SysFont("Times New Roman", 24)

    # Координаты кнопок
    button_width = 300
    button_height = 50
    left_button_rect = pygame.Rect(50, frame_height + 25, button_width, button_height)
    right_button_rect = pygame.Rect(frame_width - button_width - 50, frame_height + 25, button_width, button_height)

    # Запускаем видео
    cap = cv2.VideoCapture(video_path)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Проверяем нажатие кнопок
            if event.type == pygame.MOUSEBUTTONDOWN:
                if left_button_rect.collidepoint(event.pos):
                    print("Спасибо! Угроза устранена")
                    running = False  # Закрываем окно
                    timer=30
                elif right_button_rect.collidepoint(event.pos):
                    print("Ошибка! Будь внимательнее!")
                    running = False  # Закрываем окно
                    timer=30
        # Рисуем фон
        screen.fill(background_color)

        # Отображаем видео
        ret, frame = cap.read()
        if not ret:
            break  # Если видео закончилось

        # Исправляем изображение: поворачиваем и зеркально отражаем
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # Поворот на 90 градусов против часовой стрелки
        frame = cv2.flip(frame, 2)  # Зеркальное отражение по вертикальной оси

        # Конвертируем цвета
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Преобразуем в Pygame Surface
        resized_frame = pygame.surfarray.make_surface(cv2.resize(frame, (frame_width//16*9, frame_height//9*16)))

        # Центрируем изображение в окне
        x_offset = (frame_width-frame_width//16*9)//5
        y_offset = 0
        screen.blit(resized_frame, (x_offset, y_offset))

        # Рисуем кнопки
        mouse_pos = pygame.mouse.get_pos()
        left_color = button_hover_color if left_button_rect.collidepoint(mouse_pos) else button_color
        right_color = button_hover_color if right_button_rect.collidepoint(mouse_pos) else button_color

        pygame.draw.rect(screen, left_color, left_button_rect)
        pygame.draw.rect(screen, right_color, right_button_rect)

        # Добавляем текст на кнопки
        left_text = font.render("Спасибо! Угроза устранена", True, text_color)
        right_text = font.render("Ошибка! Будь внимательнее!", True, text_color)

        screen.blit(left_text, left_text.get_rect(center=left_button_rect.center))
        screen.blit(right_text, right_text.get_rect(center=right_button_rect.center))

        # Обновляем экран
        pygame.display.flip()
        clock.tick(30)

    cap.release()
    pygame.quit()
    time.sleep(timer)



def start_recording(sec):
    """
    Основной цикл записи видео с камер и анализа.
    """
    time.sleep(sec)
    while True:
        index = 1
        for i in url:
            cap = cv2.VideoCapture(i.strip())
            if not cap.isOpened():
                print(f"Не удалось подключиться к камере: {i}")
                continue
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_path = f"./for_video/phone{index}.mp4"
            os.makedirs(os.path.dirname(video_path), exist_ok=True)
            out = cv2.VideoWriter(video_path, fourcc, fps,
                                  (frame_width, frame_height))
            start_time = time.time()

            while time.time() - start_time < video_duration:
                ret, frame = cap.read()
                if not ret:
                    print("Не удалось получить кадр. Проверьте подключение к камере.")
                    break
                frame = cv2.resize(frame, (frame_width, frame_height))
                out.write(frame)
            out.release()
            cap.release()
            analyze_video(video_path, index, i.strip())
            index += 1


if __name__ == "__main__":
    start_recording(0)
