import serial
import threading
from datetime import datetime
import time

stop_flag = False   # Shared flag to stop all threads

def read_arduino(port, filename):
    global stop_flag
    ser = serial.Serial(port, 9600, timeout=1)

    with open(filename, "w") as f:
        while not stop_flag:
            try:
                line = ser.readline().decode(errors='ignore').strip()
                if line:
                    timestamp = datetime.now().isoformat()
                    f.write(f"{timestamp}, {line}\n")
                    print(port, line)
            except Exception as e:
                print(f"Error reading {port}: {e}")
                break

    ser.close()
    print(f"{port} closed.")

# Start threads
t1 = threading.Thread(target=read_arduino, args=("COM3", "arduino1.csv"))
t2 = threading.Thread(target=read_arduino, args=("COM11", "arduino2.csv"))

t1.start()
t2.start()

try:
    # Keep main thread alive
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopping…")
    stop_flag = True

# Wait for threads to end
t1.join()
t2.join()

print("All logging stopped safely.")
