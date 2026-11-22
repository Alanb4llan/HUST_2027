#include <STM32_CAN.h>
#include "STM32_CAN.h"
#include "LoRafunc.h"
#include "CANfunc.h"

void setup() {
  Serial.begin(115200);
  
  Can.begin();
  Can.setBaudRate(500000); // 500kbps

//-----------------Filters--------------------------//
  Can.setAutoBusOffRecovery(true); // Recover from EMI/Noise
  Can.setIRQPriority(5, 0);        // Higher priority than standard tasks
  //Motor Controller (Allows 0x400 to 0x40F)
  Can.setFilterSingleMask(0, 0x400, 0x7F0, STD); 
  
  // BMS (Allows 0x600 to 0x607)
  Can.setFilterSingleMask(1, 0x600, 0x7F8, STD);
  
  //MPPTs (Allows 0x200 to 0x23F)  
  Can.setFilterSingleMask(2, 0x200, 0x7C0, STD);
  
  Serial.println("STM32 Solar Car Controller Initialized");
    
  pinMode(PA10, OUTPUT); 
  pinMode(PA8, OUTPUT); //RIGHT INDICATOR
  pinMode(PA9, OUTPUT); //LEFT INDICATOR
}

void loop() {

  CanReadAll();
  if (millis() - prevmsg > 100) {
    printTelemetryToSerial();
    prevmsg = millis();
  }

  sendConsolidatedPacket();

  digitalWrite(PA10, HIGH); //Brake lights
  digitalWrite(PA8, HIGH); //RIGHT INDICATOR
  digitalWrite(PA9, HIGH); //LEFT INDICATOR
  
}