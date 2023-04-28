#include "DHT.h"

#define DHTPIN 3
#define DHTTYPE DHT11   // DHT 11 

int BuzzerPin = 5;
const int ledPin = 4;     // the number of the LED pin, D3
int ledState = LOW;       // the state of the LED
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  // put your setup code here, to run once:
  pinMode(ledPin, OUTPUT);
  pinMode(BuzzerPin, OUTPUT);
  digitalWrite(ledPin, ledState);
  Serial.begin(9600);
  dht.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
  float temp, humi;
  int input;
  int light = analogRead(A3);
  temp = dht.readTemperature();
  humi = dht.readHumidity();
  light = map(light, 0, 800, 0, 10); // map light, 10 bright, 0 dark
  digitalWrite(ledPin, HIGH); // turn on light of LED button
  input = Serial.read();
  if (input == 10){
    analogWrite(BuzzerPin, 128);
    delay(1000);
    analogWrite(BuzzerPin, 0);
    delay(0);
  }
  if (light <= 5){
    Serial.println("Dark", temp, humi);
  } else {
    Serial.println("Light", temp, humi);
  }
  
}
