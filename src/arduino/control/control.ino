#include <RCSwitch.h>

#define ZERO 48
#define ONE 49

RCSwitch rc_switch = RCSwitch();

char system_code[6];
char device_code[6];
char buffer[128];

void setup() { 
  rc_switch.enableTransmit(10);
  Serial.begin(9600);
  system_code[5] = '\0';
  device_code[5] = '\0';
}

void loop() {
  int length = Serial.readBytesUntil('\n', buffer, 128);
  if (length == 0)
    return;
    
  // Commands are 11 chars - 0/1 for off/on, 5 chars for system code,
  // 5 chars for device code
  if (length != 11) {
    Serial.print("-1\n");
    return;
  }

  // Commands are all ASCII ones or zeros...  Sorry!
  for (int i=0; i<11; i++) {
    if (buffer[i] != ZERO && buffer[i] != ONE) {
      Serial.print("-2\n");
      return;
    }
  }

  // Copy into new buffers - need null char.
  memcpy(device_code, &buffer[6], 5);
  memcpy(system_code, &buffer[1], 5);;

  if (buffer[0] != ZERO) {
    rc_switch.switchOn(system_code, device_code);
  } else {
    rc_switch.switchOff(system_code, device_code);
  }
  
  Serial.print("1\n");
}

