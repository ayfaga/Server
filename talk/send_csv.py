import socket
import csv
import time

def send_csv(file_name, robot_id):
    with open(f"./variable_txt/robot{robot_id}/URL_robot{robot_id}.txt", "r") as f:
        HOST = f.readline().strip()  # IP-адрес сервера
    PORT = 1024  # Порт сервера
    BUFFER_SIZE = 4096  # Размер буфера для отправки данных

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
        except:
            return "NO_CONNECT"
        # Открываем CSV-файл и отправляем данные по частям
        try:
            with open(file_name, "r", encoding="utf-8") as csvfile:
                while True:
                    chunk = csvfile.read(BUFFER_SIZE)
                    if not chunk:
                        break  # Если данных больше нет, завершаем цикл
                    time.sleep(0.5)
                    client_socket.sendall(chunk.encode("utf-8"))  # Отправляем данные в UTF-8
                    
        except:
            with open(file_name, "r", encoding="windows-1251") as csvfile:
                while True:
                    chunk = csvfile.read(BUFFER_SIZE)
                    if not chunk:
                        break  # Если данных больше нет, завершаем цикл
                    time.sleep(0.1)
                    client_socket.sendall(chunk.encode("windows-1251"))  # Если не получилось, отправляем в Windows-1251
    return "OK"