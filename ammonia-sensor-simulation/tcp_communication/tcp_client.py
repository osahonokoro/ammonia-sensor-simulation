import socket

def send_to_dashboard(payload):
    host = '127.0.0.1'
    port = 5050

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(payload.encode('utf-8'))
    except ConnectionRefusedError:
        print("Dashboard server not available.")
