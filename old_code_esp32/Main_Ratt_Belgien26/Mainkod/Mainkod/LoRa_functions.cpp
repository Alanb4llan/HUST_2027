#include "LoRa_functions.h"

// Transmitting frequency
float sendInterval = 1.0;
// Spreading factor (6-12)
int sf = 7;
// Signal bandwidth (20.8e3, 62.5e3, 125e3, and 250e3)
long sbw = 125000;
extern bool LoRaOK;
SPIClass spiLoRa(FSPI);

void setupLoRa() {
  
  Serial.println("LoRa Sender");

  // Begin custom SPI
  spiLoRa.begin(SCK, MISO, MOSI, SS);

  // Setup LoRa transceiver module
  LoRa.setSPI(spiLoRa);
  LoRa.setPins(SS, RST, DIO0);

  //915-938 for Australia
  //863-870 or 433 for Sweden
  unsigned long LoRaStartTime = millis();
  while (!LoRa.begin(868E6)) {
    Serial.println(".");
    delay(500);
    if(millis() - LoRaStartTime>10000){
      LoRaOK = false;
      Serial.println("LoRa Initializing failed");
      return;
    }
  }

  // Set spreading factor
  LoRa.setSpreadingFactor(sf);
  // Set bandwidth
  LoRa.setSignalBandwidth(sbw);

  // The sync word assures you don't get LoRa messages from other LoRa transceivers
  // ranges from 0-0xFF
  LoRa.setSyncWord(0xF3);
  LoRaOK = true;
  Serial.println("LoRa Initializing OK!");
}

void sendLoRaData() {

    while(LoRa.beginPacket() == 0) {
      Serial.println("Waiting for radio...");
      delay(100);
    }

    LoRa.beginPacket();
    
    LoRa.print(velocity); LoRa.print(" ");
    LoRa.print(distance_travelled); LoRa.print(" ");
    LoRa.print(battery_volt); LoRa.print(" ");
    LoRa.print(battery_current); LoRa.print(" ");
    LoRa.print(battery_cell_LOW_volt); LoRa.print(" ");
    LoRa.print(battery_cell_HIGH_volt); LoRa.print(" ");
    LoRa.print(battery_cell_AVG_volt); LoRa.print(" ");
    LoRa.print(battery_cell_LOW_temp); LoRa.print(" ");
    LoRa.print(battery_cell_HIGH_temp); LoRa.print(" ");
    LoRa.print(battery_cell_AVG_temp); LoRa.print(" ");
    LoRa.print(battery_cell_ID_HIGH_volt); LoRa.print(" ");
    LoRa.print(battery_cell_ID_LOW_volt); LoRa.print(" ");
    LoRa.print(BMS_temp); LoRa.print(" ");
    LoRa.print(BATTERY_WATTHOURS_SINCE_START); LoRa.print(" ");
    LoRa.print(motor_current); LoRa.print(" ");
    LoRa.print(motor_temp); LoRa.print(" ");
    LoRa.print(motor_controller_temp); LoRa.print(" ");
    LoRa.print(MPPTInputPower1); LoRa.print(" ");
    LoRa.print(MPPTInputPower2); LoRa.print(" ");
    LoRa.print(MPPTInputPower3); LoRa.print(" ");
    LoRa.print(MPPTInputPower4); LoRa.print(" ");
    LoRa.print(MPPTOutputPower1); LoRa.print(" ");
    LoRa.print(MPPTOutputPower2); LoRa.print(" ");
    LoRa.print(MPPTOutputPower3); LoRa.print(" ");
    LoRa.print(MPPTOutputPower4); LoRa.print(" ");
    LoRa.print(MPPT_total_watt_out); 


    LoRa.endPacket();
    Serial.println("CAN sent with LoRa.");
}
