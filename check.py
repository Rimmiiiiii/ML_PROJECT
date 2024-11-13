import serial

try:
    arduino = serial.Serial('COM6', 9600)
    print("Port is open")
except serial.SerialException as e:
    print(f"Error opening port: {e}")
