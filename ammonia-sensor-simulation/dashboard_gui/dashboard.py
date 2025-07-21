import tkinter as tk
from tkinter import ttk
import socket
import threading
import json

# GUI setup
root = tk.Tk()
root.title("Ammonia Monitoring Dashboard")
root.geometry("400x250")
root.resizable(False, False)

# Display Variables
nh4_var = tk.StringVar(value="--")
status_var = tk.StringVar(value="Waiting...")

# GUI Layout
ttk.Label(root, text="NH₄⁺ Concentration (mg/L)", font=("Arial", 14)).pack(pady=10)
nh4_label = ttk.Label(root, textvariable=nh4_var, font=("Arial", 24))
nh4_label.pack()

ttk.Label(root, text="Sensor Status", font=("Arial", 12)).pack(pady=10)
status_label = ttk.Label(root, textvariable=status_var, font=("Arial", 18))
status_label.pack()

# Function to update GUI
def update_dashboard(data):
    try:
        payload = json.loads(data)
        nh4 = payload.get("NH4", "--")
        status = payload.get("status", "Unknown")

        nh4_var.set(f"{nh4:.2f}")
        status_var.set(status)

        if status == "ALERT":
            nh4_label.config(foreground="red")
            status_label.config(foreground="red")
        else:
            nh4_label.config(foreground="green")
            status_label.config(foreground="green")
    except json.JSONDecodeError:
        print("Invalid packet format.")

# TCP Listener in Background Thread
def tcp_server():
    host = '127.0.0.1'
    port = 5050
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Dashboard is listening on port 5050...")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                update_dashboard(data)

# Launch server listener in separate thread
threading.Thread(target=tcp_server, daemon=True).start()

# Start GUI main loop
root.mainloop()
