import serial
import threading
from datetime import datetime
import queue
import time

# ---------------- CONFIG ----------------
n = 8                       # number of values per Arduino
BAUD = 9600
PORT1 = "COM11"
PORT2 = "COM3"

recording = False
stop_program = False
current_letter_index = 0
letters = [chr(ord('A') + i) for i in range(26)]

q1 = queue.Queue()
q2 = queue.Queue()

all_data = {letter: [] for letter in letters}


# ---------------- SERIAL READER ----------------
def read_arduino(port, q):
    global stop_program
    ser = serial.Serial(port, BAUD, timeout=1)

    while not stop_program:
        try:
            line = ser.readline().decode(errors="ignore").strip()
        except:
            continue

        if not line:
            continue

        parts = line.split()

        # STRICT validation for n = 13
        if len(parts) != n:
            continue

        # Ensure numeric data
        try:
            [float(x) for x in parts]
        except ValueError:
            continue

        q.put(parts)

    ser.close()


# ---------------- COMBINER ----------------
def combiner():
    global recording, stop_program, current_letter_index

    while not stop_program:
        if not recording:
            time.sleep(0.05)
            continue

        try:
            v1 = q1.get(timeout=0.2)
            v2 = q2.get(timeout=0.2)
        except queue.Empty:
            continue

        letter = letters[current_letter_index]
        timestamp = datetime.now().isoformat()

        row = [timestamp, letter] + v1 + v2
        all_data[letter].append(row)

        print(f"[{letter}] A1={v1} | A2={v2}")


# ---------------- THREADS ----------------
t1 = threading.Thread(target=read_arduino, args=(PORT1, q1), daemon=True)
t2 = threading.Thread(target=read_arduino, args=(PORT2, q2), daemon=True)
tc = threading.Thread(target=combiner, daemon=True)

t1.start()
t2.start()
tc.start()

print("\nPress ENTER → START recording letter A")
print("Press ENTER → STOP and move to next letter")
print("Will continue A → Z\n")

# ---------------- CONTROL LOOP ----------------
try:
    while current_letter_index < 26:
        input()
        recording = not recording

        if recording:
            print(f"\n▶ STARTED recording {letters[current_letter_index]}")
        else:
            print(f"\n■ STOPPED recording {letters[current_letter_index]}")

            # flush queues to avoid mixing letters
            with q1.mutex:
                q1.queue.clear()
            with q2.mutex:
                q2.queue.clear()

            current_letter_index += 1

            if current_letter_index < 26:
                print(f"Next ENTER will start letter {letters[current_letter_index]}")

except KeyboardInterrupt:
    print("\nStopping…")

stop_program = True
time.sleep(0.5)


# ---------------- SAVE CSV ----------------
tstamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"en_2x12_{tstamp}.csv"

with open(filename, "w") as f:
    header = (
        "timestamp,letter,"
        + ",".join([f"A1_v{i}" for i in range(1, n + 1)]) + ","
        + ",".join([f"A2_v{i}" for i in range(1, n + 1)]) + "\n"
    )
    f.write(header)

    for letter in letters:
        for row in all_data[letter]:
            f.write(",".join(row) + "\n")

print(f"\n📁 Saved CSV with {n} values per Arduino → {filename}")
print("Done.")
