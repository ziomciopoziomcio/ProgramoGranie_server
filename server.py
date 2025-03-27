import socket
import threading
import json

def handle_client(client_socket):
    try:
        try:
            data_original = client_socket.recv(1024).decode('utf-8')
            data = json.loads(data_original)
        except Exception as e:
            return
        # FUNCTIONALITY
        return
    finally:
        client_socket.close()


def start_server(host = '', port = 12345):
    # REMEMBER TO CREATE CLEANUP MECHANISM
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    while True:
        client_socket, _ = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()
