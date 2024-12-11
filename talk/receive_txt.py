import socket

HOST = ''  # Введите IP-адрес принимающего ноутбука (или оставьте пустым для привязки ко всем интерфейсам)
PORT = 1024  # Любой свободный порт (например, 12345)

def receive_file():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Сервер запущен на {HOST}:{PORT}, ожидает соединения...")
        
        conn, addr = server_socket.accept()
        print(f"Соединение установлено с {addr}")
        
        with conn:
            file_name = "./talk/received.txt"
            with open(file_name, "wb") as f:
                while True:
                    data = conn.recv(1024)  # Получаем данные порциями
                    if not data:  # Если данные закончились
                        break
                    f.write(data)
            print(f"Файл успешно получен и сохранен как {file_name}")

if __name__ == "__main__":
    receive_file()
