const int sensorPin = A0;
const int soilPowerPin = 7;
const int tempPin = A5;
const int photoPin = A1;
const int waterPin = 2;

// Measure the voltage at 5V and the actual resistance of your
// 47k resistor, and enter them below:
const float VCC = 5.10; // Measured voltage of Ardunio 5V line
const float R_DIV = 4620.0; // Measured resistance of 4.7k resistor

// Remote commands
char buff[3] = "  ";
unsigned short controlChars = 0;
volatile unsigned short timer1Counter = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(soilPowerPin, OUTPUT);
  pinMode(waterPin, OUTPUT);

  // initialize timer1 
  noInterrupts();           // disable all interrupts
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1  = 0;

  // (CPU CLK Speed/ Prescaler) / Desired Hz
  // ((16*10^6) / 1024) / (1/60) = 937,500
  // Once a minute (this is too large) Max is 65,536
  // If we divide by 15, we get a number smaller than the Max = 62,500
  // So we will count up to 15 and trigger
  OCR1A = 0xF424;           // compare match register
  TCCR1B |= (1 << WGM12);   // CTC mode (clear timer on compare match)
  TCCR1B |= (1 << CS10);    // 1024 prescaler 
  TCCR1B |= (1 << CS12);
  TIMSK1 |= (1 << OCIE1A);  // enable timer compare interrupt
  interrupts();             // enable all interrupts

  Serial.begin(9600);
}

// timer compare interrupt service routine
ISR(TIMER1_COMPA_vect) {
  if (++timer1Counter == 15) {
    timer1Counter = 0;
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
  }
}

void loop() {
  char buffer1;
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    buffer1 = Serial.read();
    if (controlChars == 0 || controlChars == 1) {
      buff[controlChars] = buffer1;
    }
    if (++controlChars == 2) {
      controlChars = 0;
    }

    if (controlChars == 0) {
      if (strcmp(buff, "W1") == 0) {
        digitalWrite(waterPin, HIGH);
      } else {
        digitalWrite(waterPin, LOW);
      }
    }
  }
  delay(10);
}
