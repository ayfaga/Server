import socket

def receive_csv(file_path):
    HOST = ''  # IP-адрес сервера
    PORT = 1024  # Порт сервера
    BUFFER_SIZE = 4096  # Размер буфера для чтения данных
    temp_buffer = ""  # Временный буфер для хранения незаконченной строки

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Сервер запущен на {HOST}:{PORT}, ожидает соединения...")

        conn, addr = server_socket.accept()
        print(f"Соединение установлено с {addr}")
        try:
            with conn, open(file_path, "w", newline='', encoding="utf-8") as csvfile:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break  # Если данных больше нет, завершаем цикл

                    # Попробуем декодировать данные
                    
                    chunk = data.decode("utf-8")

                    # Добавляем новые данные к временной строке
                    temp_buffer += chunk

                    # Делим буфер на строки
                    lines = temp_buffer.split("\n")

                    # Все строки, кроме последней, записываем в файл
                    for line in lines[:-1]:
                        csvfile.write(line + "\n")

                    # Последняя строка может быть незаконченной, оставляем её в буфере
                    temp_buffer = lines[-1]

                # Если после цикла в буфере осталась строка, записываем её в файл
                if temp_buffer:
                    csvfile.write(temp_buffer + "\n")
        except:
            with conn, open(file_path, "w", newline='', encoding="utf-8") as csvfile:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break  # Если данных больше нет, завершаем цикл

                    # Попробуем декодировать данные
                    
                    chunk = data.decode("utf-8")

                    # Добавляем новые данные к временной строке
                    temp_buffer += chunk

                    # Делим буфер на строки
                    lines = temp_buffer.split("\n")

                    # Все строки, кроме последней, записываем в файл
                    for line in lines[:-1]:
                        csvfile.write(line + "\n")

                    # Последняя строка может быть незаконченной, оставляем её в буфере
                    temp_buffer = lines[-1]

                # Если после цикла в буфере осталась строка, записываем её в файл
                if temp_buffer:
                    csvfile.write(temp_buffer + "\n")

        print(f"Данные сохранены в файл {file_path}")
