# # sum_reader.py
# from arduino_reader import start_readers, read_combined
# import time
# start_readers()   # start Arduino reading threads

# print("Real-time sum processor running...\n")

# total = None  # exported

# def _process():
#     global total
#     for values in read_combined():
#         total = chr(int(sum(values)*10) +75)
#         # print(f"Sum: {total}")
#         # time.sleep(1)
#     return total
# # _process()


# sum_module.py
from arduino_reader import start_readers, read_combined
import threading
import time

total = None  # exported

def _process():
    global total
    for values in read_combined():
        total = chr(int(sum(values)*10) + 80)

def start():
    # time.sleep(1)  # wait for serial connections
    start_readers()
    t = threading.Thread(target=_process)
    t.daemon = True
    t.start()
