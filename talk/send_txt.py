import socket

def send_file(file_name, robot_id):
    with open(f"./variable_txt/robot{robot_id}/URL_robot{robot_id}.txt", "r", encoding='utf8') as f:
        HOST = f.readline().strip()  # IP-адрес сервера
    PORT = 1024  # Порт сервера
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
        except:
            return "NO_CONNECT"
        
        with open(file_name, "rb") as f:
            while chunk := f.read(1024):  # Читаем файл порциями
                client_socket.sendall(chunk)
    return "OK"

if __name__ == "__main__":
    file_name = "./talk/send.txt"  # Имя файла, который вы хотите отправить
    send_file(file_name)
