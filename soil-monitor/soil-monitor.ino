const int sensorPin = A0;
const int powerPin = 7;

void setup() {
  // put your setup code here, to run once:
  pinMode(powerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(powerPin, HIGH);
  int val = analogRead(sensorPin);
  digitalWrite(powerPin, LOW);
  Serial.println(val);
  delay(60000);
}
