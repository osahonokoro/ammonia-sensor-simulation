import random
import time

def emulate_apure_sensor():
    while True:
        concentration = round(random.uniform(0.0, 10.0), 2)
        register_value = int(concentration * 10)  # Scaled value for Modbus register
        status = "HIGH" if concentration > 5.0 else "NORMAL"

        modbus_packet = {
            'register': '0x03F1',
            'raw_value': register_value,
            'concentration_mg_L': concentration,
            'status_flag': status
        }

        print(modbus_packet)
        time.sleep(5)  # Simulated polling interval

emulate_apure_sensor()
