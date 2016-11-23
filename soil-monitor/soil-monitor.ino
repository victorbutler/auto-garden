const int sensorPin = A0;
const int soilPowerPin = 7;
const int tempPin = A5;
const int photoPin = A1;

// Measure the voltage at 5V and the actual resistance of your
// 47k resistor, and enter them below:
const float VCC = 5.10; // Measured voltage of Ardunio 5V line
const float R_DIV = 4620.0; // Measured resistance of 4.7k resistor

void setup() {
  // put your setup code here, to run once:
  pinMode(soilPowerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int photoReading = analogRead(photoPin);
  float photoVoltage = photoReading * (VCC / 1023.0);
  float photoResistance = R_DIV * (VCC / photoVoltage - 1.0);
  digitalWrite(soilPowerPin, HIGH);
  int soilReading = analogRead(sensorPin);
  digitalWrite(soilPowerPin, LOW);
  int tempReading = analogRead(tempPin);
  float voltage = (tempReading * 5.0) / 1024;
  float tempC = (voltage - 0.5) * 100;
  float tempF = ((tempC * 9.0) / 5.0) + 32;
  Serial.print(soilReading);
  Serial.print(", ");
  Serial.print(tempF);
  Serial.print(", ");
  Serial.println(photoResistance);
  delay(60000);
}
