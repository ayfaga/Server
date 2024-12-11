import socket
import time
import pygame
from talk.send_csv import send_csv
from talk.receive_csv import receive_csv
HOST = ''  # Введите IP-адрес принимающего ноутбука (или оставьте пустым для привязки ко всем интерфейсам)
PORT = 1024  # Любой свободный порт (например, 12345)
while 1:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Сервер запущен на {HOST}:{PORT}, ожидает соединения...")
        
        conn, addr = server_socket.accept()
        print(f"Соединение установлено с {addr}")
        
        with conn:
            file_name = "./talk/received.txt"
            data = ''
            with open(file_name, "wb") as f:
                while True:
                    data2 = conn.recv(1024)  # Получаем данные порциями
                    if not data2:  # Если данные закончились
                        break
                    f.write(data2)