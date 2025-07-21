import time
import random

def get_sensor_value():
    # Simulate Modbus register value (0–100)
    return random.randint(0, 100)

def send_to_dashboard(payload):
    print("Sending:", payload)

while True:
    raw_register = get_sensor_value()
    concentration = raw_register / 10.0
    status = "ALERT" if concentration > 5.0 else "NORMAL"

    packet = {
        "NH4": round(concentration, 2),
        "status": status
    }

    send_to_dashboard(packet)
    time.sleep(5)
