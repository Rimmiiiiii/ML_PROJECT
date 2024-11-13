# Step 1: List all available ports to check if COM5 is detected
ports = list(serial.tools.list_ports.comports())
print("Available Ports:")
for port in ports:
    print(port.device)

# Step 2: Add a delay to ensure the Arduino is recognized by the system
time.sleep(2)  # Wait for 2 seconds

try:
    # Step 3: Open the serial connection with a timeout
    arduino = serial.Serial('COM6', 9600, timeout=1)
    print("Connection established on COM6")
except serial.SerialException as e:
    print(f"Failed to connect to COM6: {e}")
    exit(1)  # Exit if the port is not accessible

# Step 4: Add code to read data (as an example)
try:
    while True:
        if arduino.in_waiting > 0:
            data = arduino.readline().decode('utf-8').strip()
            print(f"Received data: {data}")
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    # Step 5: Clean up by closing the serial connection
    if arduino.is_open:
        arduino.close()
        print("Serial connection closed.") 