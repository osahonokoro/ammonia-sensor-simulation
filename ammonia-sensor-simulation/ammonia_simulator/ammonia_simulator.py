import tkinter as tk
from tkinter import ttk
import socket
import threading
import json
import random
import time
import csv
from datetime import datetime

# ---------- GUI Setup ----------
root = tk.Tk()
root.title("Ammonia Monitoring Dashboard")
root.geometry("400x250")
root.resizable(False, False)

nh4_var = tk.StringVar(value="--")
status_var = tk.StringVar(value="Waiting...")

ttk.Label(root, text="NH₄⁺ Concentration (mg/L)", font=("Arial", 14)).pack(pady=10)
nh4_label = ttk.Label(root, textvariable=nh4_var, font=("Arial", 24))
nh4_label.pack()

ttk.Label(root, text="Sensor Status", font=("Arial", 12)).pack(pady=10)
status_label = ttk.Label(root, textvariable=status_var, font=("Arial", 18))
status_label.pack()

# ---------- Dashboard Update ----------
def update_dashboard(payload):
    nh4 = payload.get("NH4", "--")
    status = payload.get("status", "Unknown")

    nh4_var.set(f"{nh4:.2f}")
    status_var.set(status)

    color = "green" if status == "NORMAL" else "red"
    nh4_label.config(foreground=color)
    status_label.config(foreground=color)

# ---------- CSV Logger ----------
def log_to_csv(payload):
    with open("packet_log.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            payload.get("timestamp"),
            payload.get("NH4"),
            payload.get("status")
        ])

# ---------- TCP Server ----------
def start_dashboard_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 5050))
        server.listen()
        print("Dashboard is listening on port 5050...")
        while True:
            conn, _ = server.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                try:
                    payload = json.loads(data)
                    update_dashboard(payload)
                    log_to_csv(payload)
                    print("Received:", payload)
                except json.JSONDecodeError:
                    print("Invalid packet received.")

# ---------- Sensor Data Generator ----------
def generate_sensor_data():
    while True:
        raw_value = random.randint(0, 100)
        concentration = raw_value / 10.0
        status = "NORMAL" if concentration <= 4.0 else "ALERT"

        packet = {
            "NH4": concentration,
            "status": status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("127.0.0.1", 5050))
                s.send(json.dumps(packet).encode('utf-8'))
        except ConnectionRefusedError:
            print("Dashboard not ready, retrying...")

        time.sleep(2)

# ---------- Launch Threads ----------
threading.Thread(target=start_dashboard_server, daemon=True).start()
threading.Thread(target=generate_sensor_data, daemon=True).start()

# ---------- Start GUI ----------
root.mainloop()
