import serial
import time
import serial.tools.list_ports
import random  # For random water prediction

# Step 1: List all available ports to check if COM6 is detected
ports = list(serial.tools.list_ports.comports())
print("Available Ports:")
for port in ports:
    print(port.device)

# Step 2: Add a delay to ensure the Arduino is recognized by the system
time.sleep(2)  # Wait for 2 seconds to ensure the Arduino is recognized

try:
    # Step 3: Open the serial connection with a timeout
    arduino = serial.Serial('COM6', 9600, timeout=1)
    print("Connection established on COM6")
except serial.SerialException as e:
    print(f"Failed to connect to COM6: {e}")
    exit(1)  # Exit if the port is not accessible

# Step 4: Record sensor values at an interval of 1 minute and make water predictions
try:
    while True:
        # Check if there is data available from the Arduino
        if arduino.in_waiting > 0:
            # Read data from the serial port
            data = arduino.readline().decode('utf-8').strip()
            print(f"Received data: {data}")
            
            # Simulate water prediction based on the received data
            water_prediction = random.uniform(2, 3)  # Random water prediction between 2 and 3
            print(f"Predicted Water Amount: {water_prediction:.2f} liters")
            
            # Check water level condition
            if "Water Level:" in data and "very low" in data.lower():
                print("Pump OFF: No water needed.")
            else:
                print("Pump ON: Water needed.")
        
        # Wait for 1 minute before reading and predicting the next value
        time.sleep(15)  # Sleep for 60 seconds (1 minute)

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    # Step 5: Clean up by closing the serial connection
    if arduino.is_open:
        arduino.close()
        print("Serial connection closed.")
