#include <Arduino.h>

void setup();
void loop();
#line 1 "src/sketch.ino"
String data;
boolean flag=false;
int led = 13;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led, OUTPUT);  
}

void loop() {
  data = Serial.readString();
  
  if(data == "on"){
    digitalWrite(led, HIGH);
    Serial.print("1\n");
  } else if(data == "off"){
    digitalWrite(led, LOW);
    Serial.print("0\n");
  } else {
    Serial.print(data);
  }

  // delay(1);
}

/*
  digitalWrite(led, HIGH);
 digitalWrite(led, LOW);
 */


