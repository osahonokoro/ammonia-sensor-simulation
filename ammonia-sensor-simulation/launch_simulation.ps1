# Define the root path of your simulation
$basePath = "C:\Users\Otala\Desktop\Osahon\Project 2025\Jude\git_repo\ammonia-sensor-simulation"

# Launch Sensor Emulator
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$basePath\sensor_emulator'; python sensor_emulator.py"

# Launch ESP32 Emulator
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$basePath\esp32_emulator'; python esp32_logic_sim.py"

# Launch TCP Server (Dashboard)
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$basePath\tcp_communication'; python tcp_server.py"

# Launch GUI Dashboard
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$basePath\dashboard_gui'; python dashboard.py"
