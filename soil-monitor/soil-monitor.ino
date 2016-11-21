const int sensorPin = A0;
const int soilPowerPin = 7;
const int tempPin = A5;

void setup() {
  // put your setup code here, to run once:
  pinMode(soilPowerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(soilPowerPin, HIGH);
  int soilReading = analogRead(sensorPin);
  digitalWrite(soilPowerPin, LOW);
  int tempReading = analogRead(tempPin);
  float voltage = (tempReading * 5.0) / 1024;
  float tempC = (voltage - 0.5) * 100;
  float tempF = ((tempC * 9.0) / 5.0) + 32;
  Serial.print(soilReading);
  Serial.print(", ");
  Serial.println(tempF);
  // Serial.println("°F");
  delay(60000);
}
