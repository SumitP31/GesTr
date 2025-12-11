import serial
import threading
from datetime import datetime
import queue
import time

recording = False
stop_program = False
current_letter_index = 0
letters = [chr(ord('A') + i) for i in range(26)]

# Two queues for Arduino data
q1 = queue.Queue()
q2 = queue.Queue()

# Storage for all combined A→Z data
all_data = {letter: [] for letter in letters}


def read_arduino(port, q):
    """Reads from one Arduino and pushes raw 7-value line to queue."""
    global stop_program

    ser = serial.Serial(port, 9600, timeout=1)

    while not stop_program:
        try:
            line = ser.readline().decode(errors='ignore').strip()
        except:
            continue

        if line:
            q.put(line)   # Save raw line like "120 350 220 140 500 600 700"

    ser.close()


def combiner():
    """Combines A1 & A2 into single row when recording is ON."""
    global recording, stop_program, current_letter_index

    while not stop_program:
        if recording:
            try:
                raw1 = q1.get(timeout=0.1)
                raw2 = q2.get(timeout=0.1)
            except queue.Empty:
                continue

            # Split into 7 columns each
            v1 = raw1.split()
            v2 = raw2.split()

            if len(v1) != 7 or len(v2) != 7:
                continue  # skip malformed data lines

            letter = letters[current_letter_index]
            timestamp = datetime.now().isoformat()

            # Build CSV row
            row = [timestamp, letter] + v1 + v2
            all_data[letter].append(row)

            print(f"[{letter}] A1={v1} | A2={v2}")

        else:
            time.sleep(0.05)


# ------------------ Start threads ------------------
t1 = threading.Thread(target=read_arduino, args=("COM3", q1))
t2 = threading.Thread(target=read_arduino, args=("COM11", q2))
tc = threading.Thread(target=combiner)

t1.start()
t2.start()
tc.start()

print("\nPress ENTER → START recording letter A")
print("Press ENTER → STOP and move to next letter")
print("Will continue A → Z\n")

try:
    while current_letter_index < 26:
        input()  # Toggle recording
        recording = not recording

        if recording:
            print(f"\n▶ STARTED recording {letters[current_letter_index]}")
        else:
            print(f"\n■ STOPPED recording {letters[current_letter_index]}")
            current_letter_index += 1

            if current_letter_index >= 26:
                print("\n✔ Finished all letters A → Z.")
                break
            else:
                print(f"Next ENTER will start letter {letters[current_letter_index]}")

except KeyboardInterrupt:
    print("\nStopping…")

stop_program = True

t1.join()
t2.join()
tc.join()

# ------------------ Save CSV ------------------
filename = "A_to_Z_combined_7_values.csv"

with open(filename, "w") as f:
    header = (
        "timestamp,letter,"
        + ",".join([f"A1_v{i}" for i in range(1, 8)]) + ","
        + ",".join([f"A2_v{i}" for i in range(1, 8)]) + "\n"
    )
    f.write(header)

    for letter in letters:
        for row in all_data[letter]:
            f.write(",".join(row) + "\n")

print(f"\n📁 Saved CSV with 7 columns per Arduino → {filename}")
print("Done.")
