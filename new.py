import serial
import time
import serial.tools.list_ports
import random  # For random water prediction

# Step 1: List all available ports to check if COM6 is detected
ports = list(serial.tools.list_ports.comports())
print("Available Ports:")
for port in ports:
    print(port.device)

# Step 2: Delay to ensure Arduino is recognized by the system
time.sleep(2)

try:
    # Step 3: Open the serial connection with reduced timeout
    arduino = serial.Serial('COM6', 9600, timeout=0.5)
    print("Connection established on COM6")
except serial.SerialException as e:
    print(f"Failed to connect to COM6: {e}")
    exit(1)

# Track time for 2-minute interval
last_print_time = time.time() - 120  # Ensure first data print is immediate

try:
    while True:
        # Check if data is available from Arduino
        if arduino.in_waiting > 0:
            # Read data and parse sensor values safely
            try:
                data = arduino.readline().decode('utf-8').strip()
                print(f"Received data: {data}")

                # Parse sensor values in format: "LDR:123, Ultrasonic:10, Temp:25, Humidity:60, Light Intensity:500"
                sensor_values = {}
                for item in data.split(", "):
                    key, value = item.split(":")
                    sensor_values[key.strip()] = float(value.strip())

                # Extract sensor values with fallback to 0 if unavailable
                ldr_value = sensor_values.get("LDR", 0)
                ultrasonic_value = sensor_values.get("Ultrasonic", 0)
                temp_value = sensor_values.get("Temp", 0)
                light_intensity = sensor_values.get("Light Intensity", 0)

                # Check if 2 minutes have passed since the last print
                current_time = time.time()
                if current_time - last_print_time >= 120:
                    # Print all sensor values excluding humidity
                    print(f"LDR Value: {ldr_value}")
                    print(f"Ultrasonic Value: {ultrasonic_value}")
                    print(f"Temperature: {temp_value} °C")
                    print(f"Light Intensity: {light_intensity} lux")

                    # Simulate water prediction based on ultrasonic sensor value
                    if ultrasonic_value < 200:
                        water_prediction = 0.00
                        print("Pump OFF: No water needed.")
                        arduino.write(b'PUMP_OFF\n')  # Send command to turn off the pump
                    else:
                        water_prediction = random.uniform(2, 3)
                        print("Pump ON: Water needed.")
                        arduino.write(b'PUMP_ON\n')  # Send command to turn on the pump

                    # Display the predicted water amount in the terminal window
                    print(f"Predicted Water Amount: {water_prediction:.2f} liters")

                    # Update the last print time
                    last_print_time = current_time

            except ValueError as e:
                print(f"Data parsing error: {e}")  # Skip and continue on parsing errors

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    # Step 5: Close the serial connection on exit
    if arduino.is_open:
        arduino.close()
        print("Serial connection closed.")
