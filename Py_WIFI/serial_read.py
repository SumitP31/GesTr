import socket

HOST = "192.168.4.1"   # Arduino AP IP
PORT = 8080            # Same port used in Arduino code

# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to Arduino AP...")
s.connect((HOST, PORT))
print("Connected! Receiving data...\n")

try:
    while True:
        data = s.recv(1024)   # Read bytes from Arduino
        if not data:
            break
        print(data.decode().strip())  # Convert to string and print
except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    s.close()