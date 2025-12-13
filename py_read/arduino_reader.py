# arduino_reader.py
import serial
import threading
import time

N = 8  # number of values per Arduino
data_a1 = None
data_a2 = None
lock = threading.Lock()
stop_flag = False

def _read(port, name):
    global data_a1, data_a2, stop_flag
    ser = serial.Serial(port, 9600, timeout=1)

    while not stop_flag:
        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            continue

        values = line.split()
        if len(values) != N:
            continue

        with lock:
            if name == "A1":
                data_a1 = values
            else:
                data_a2 = values

    ser.close()


def start_readers(port1="COM11", port2="COM3"):
    t1 = threading.Thread(target=_read, args=(port1, "A1"))
    t2 = threading.Thread(target=_read, args=(port2, "A2"))
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()


def read_combined():
    """Generator: yields one synchronized 14-value list on each cycle."""
    global data_a1, data_a2

    while True:
        time.sleep(0.001)  # ultra low delay

        with lock:
            if data_a1 is not None and data_a2 is not None:
                combined = data_a1 + data_a2
                # print("Combined:", combined)
                # reset for next synchronized read
                data_a1 = None
                data_a2 = None

                yield list(map(float, combined))  # return numeric list


read_combined()