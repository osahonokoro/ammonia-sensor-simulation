import socket

def start_dashboard_server():
    host = '127.0.0.1'
    port = 5050

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print("Dashboard listening...")
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024).decode('utf-8')
            print("Received:", data)
