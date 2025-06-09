import os
import subprocess
import sys

def install_requirements():
    """Installs required Python packages."""
    if not os.path.exists('requirements.txt'):
        print("Plik `requirements.txt` nie istnieje. Upewnij się, że jest w katalogu projektu.")
        sys.exit(1)

    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("Wszystkie wymagane biblioteki zostały zainstalowane.")
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas instalacji bibliotek: {e}")
        sys.exit(1)

def run_server():
    """Runs the server.py file."""
    try:
        subprocess.check_call([sys.executable, 'server.py'])
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas uruchamiania serwera: {e}")
        sys.exit(1)

if __name__ == '__main__':
    install_requirements()
    run_server()