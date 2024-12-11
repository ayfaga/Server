import subprocess
import sys
python_path = sys.executable

# Запуск файлов параллельно
def run_files_parallel():
    subprocess.Popen([python_path, 'frontend_server.py'])
    subprocess.Popen([python_path, 'htmlserver.py'])
    subprocess.Popen([python_path, 'updating_data.py'])
    subprocess.Popen([python_path, 'cameras.py'])

# Запуск параллельного выполнения
if __name__ == "__main__":
    run_files_parallel()
