#include <DHT.h>

// Define pins for sensors and actuators
const int trustechPin = A0;      // Trustech soil moisture sensor connected to A0
const int rees52Pin = A1;        // REES52 soil moisture sensor connected to A1
const int buzzerPin = 8;         // Buzzer connected to pin 8
const int ledPin = 9;            // LED connected to pin 9
const int ldrPin = A2;           // LDR connected to A2
const int dhtPin = 5;            // DHT11 sensor connected to pin 5
const int triggerPin = 7;        // Ultrasonic sensor trigger connected to pin 7
const int echoPin = 6;           // Ultrasonic sensor echo connected to pin 6
const int relayPin = 10;         // Relay connected to pin 10 to control the water pump

DHT dht(dhtPin, DHT11);          // Initialize DHT sensor

unsigned long pumpOnTime = 0;    // Variable to store the time when pump was turned on
const unsigned long pumpDuration = 10000; // 10 seconds

void setup() {
  Serial.begin(9600);            // Initialize serial communication
  pinMode(buzzerPin, OUTPUT);    // Set buzzer as output
  pinMode(ledPin, OUTPUT);       // Set LED as output
  pinMode(triggerPin, OUTPUT);   // Set trigger pin as output
  pinMode(echoPin, INPUT);       // Set echo pin as input
  pinMode(relayPin, OUTPUT);     // Set relay as output
  dht.begin();                   // Start the DHT11 sensor
}

void loop() {
  // Read soil moisture levels
  int trustechMoisture = analogRead(trustechPin); // Read Trustech moisture level
  int rees52Moisture = analogRead(rees52Pin);     // Read REES52 moisture level
  int ldrValue = analogRead(ldrPin);              // Read LDR value
  float humidity = dht.readHumidity();            // Read humidity from DHT11
  float temperature = dht.readTemperature();      // Read temperature from DHT11
  int averageMoisture = (trustechMoisture + rees52Moisture) / 2;

  // Measure distance with ultrasonic sensor
  long duration, distance;
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration * 0.034) / 2; // Calculate distance in cm

  // Print sensor data to the serial monitor
  Serial.print("Average Soil Moisture Level: ");
  Serial.println(averageMoisture);
  Serial.print("LDR Value: ");
  Serial.println(ldrValue);
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print("%, Temperature: ");
  Serial.print(temperature);
  Serial.print("°C, Water Level: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Check ultrasonic distance to turn off pump if below 200 cm
  if (distance < 200) {
    digitalWrite(relayPin, LOW);  // Deactivate relay if distance is below threshold
    Serial.println("Pump OFF: Distance less than 200 cm, no water needed.");
    pumpOnTime = 0; // Reset the pump on time
  } else {
    // Check for commands from Streamlit app
    if (Serial.available() > 0) {
      String command = Serial.readStringUntil('\n');  // Read command as a string

      // Control relay based on command
      if (command == "PUMP_ON") {
        digitalWrite(relayPin, HIGH);  // Activate the relay to turn on the pump
        Serial.println("Pump ON: Command received to activate water pump.");
        pumpOnTime = millis();  // Record the time when the pump was turned on
      } 
      else if (command == "PUMP_OFF") {
        digitalWrite(relayPin, LOW);   // Deactivate the relay to turn off the pump
        Serial.println("Pump OFF: Command received to deactivate water pump.");
        pumpOnTime = 0; // Reset the pump on time
      }
    }
  }

  // Turn off the relay after 10 seconds (10000 milliseconds)
  if (pumpOnTime > 0 && millis() - pumpOnTime >= pumpDuration) {
    digitalWrite(relayPin, LOW);  // Deactivate the relay after 10 seconds
    Serial.println("Pump OFF: Automatically turned off after 10 seconds.");
    pumpOnTime = 0;  // Reset the pump on time
  }

  delay(1000); // Wait for a second before the next reading
}
