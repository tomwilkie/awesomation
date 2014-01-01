#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();

void setup() { 
  mySwitch.enableTransmit(10);
  Serial.begin(9600);
}

char* systemCode = "01010";
char* codes[] = { "10000", "01000", "00100", "00010", "00001" };
char buffer[128];

#define ZERO 48

void loop() {
  int length = Serial.readBytesUntil('\n', buffer, 128);
  if (length == 0)
      return;

  if (length != 2) {
    Serial.print("0\n");
    return;
  }
    
  char mode = buffer[0];
  char code = buffer[1];
  if (code < ZERO || code > ZERO + 5) {
    Serial.print("0\n");
    return;
  }
  int index = code - ZERO;

  if (mode != ZERO) {
    mySwitch.switchOn(systemCode, codes[index]);
  } else {
    mySwitch.switchOff(systemCode, codes[index]);
  }
  Serial.print("1\n");
}
