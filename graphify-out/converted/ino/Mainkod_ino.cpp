#include <Arduino.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "SD_card.h"
#include "CAN_functions.h"
#include "LoRa_functions.h"
#include "LED_functions.h"

// Flag for writing in same folder on the SD-card
int SDcardFlag = 1;
bool LoRaOK=false;
bool safeState=false;

void setupSD() {

  // Initialize SD
  if(!SD.begin(CS, spiLoRa)) {
    Serial.println("SD Card Mount Failed");
  } else {
    Serial.println("SD Card Mount Succesful");
  }

  // Initialize NVS
  if (initNVS()) {
    Serial.println("NVS Initialized");
  } else {
    Serial.println("NVS Initialization Failed");
  }
}

void prepareAndWrite2SD() {
  char buffer[512];
  snprintf(buffer, sizeof(buffer),
            "%.2f %.2f "
            "%.2f %.2f "
            "%.2f %.2f %.2f "
            "%.2f %.2f %.2f "
            "%.2f %.2f %.2f %.2f "
            "%.2f %.2f %.2f "
            "%.2f %.2f %.2f %.2f \n",
            velocity, distance_travelled, 
            battery_volt, battery_current, 
            battery_cell_LOW_volt, battery_cell_HIGH_volt, battery_cell_AVG_volt,
            battery_cell_LOW_temp, battery_cell_HIGH_temp, battery_cell_AVG_temp,
            battery_cell_ID_HIGH_volt, battery_cell_ID_LOW_volt, BMS_temp, BATTERY_WATTHOURS_SINCE_START,
            motor_current, motor_temp, motor_controller_temp,
            MPPTInputPower1, MPPTInputPower2, MPPTInputPower3,MPPTInputPower4,
            MPPTOutputPower1, MPPTOutputPower2, MPPTOutputPower3, MPPTOutputPower4, MPPT_total_watt_out);
  
  digitalWrite(SS, HIGH);           // Deselect LoRa
  digitalWrite(CS, LOW);            // Select SD card
  write2SDcard(buffer, SDcardFlag); // Write file to SD card
  if(SDcardFlag) SDcardFlag = 0;    // Set flag to 0 after first iteration to write on the same file
  digitalWrite(CS, HIGH);           // Deselect SD card
  digitalWrite(SS, LOW);            // Select LoRa
}

void setup() {

  delay(3000);


  //initialize Serial Monitor
  Serial.begin(115200);
  
  setupLEDs();
  
  setupLoRa();

  setupCAN();

  setupSD();
}

void loop() {
  safeState = !digitalRead(READ_SAFE_STATE);
  blinkLEDs();
  static clock_t lastSendTime = 0;
  if (ESP32Can.readFrame(msg, 0)) {
    // Assign CAN data to specified variable based on identifier
    assignCAN2variable();

    clock_t currentTime = clock();
    double timeElapsed = ((double)(currentTime - lastSendTime))/CLOCKS_PER_SEC;

    if (timeElapsed >= sendInterval) {

      sendCAN2steeringWheel(digitalRead(READ_BRAKE_LIGHT),safeState);
      Serial.printf("Safe state: %s\n", safeState ? "true" : "false");
      // Send with LoRa
      if(LoRaOK){
        sendLoRaData();
      }

      // Prepare const char of our variables and save to SD card
      prepareAndWrite2SD();

      lastSendTime = currentTime;
    }
  }

  // Check for incoming parameters from receiver
  /*
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    char receivedParams[packetSize + 1];
    int index = 0;
    while (LoRa.available()) {
      receivedParams[index++] = (char)LoRa.read();
    }
    receivedParams[index] = '\0';

    if (strncmp(receivedParams, "PARAM", 5) == 0) {
      int sf = 0, sbw = 0;
      sscanf(receivedParams, "PARAM %d %d", &sf, &sbw);

      LoRa.setSpreadingFactor(sf);
      LoRa.setSignalBandwidth(sbw);

      Serial.printf("Updated SF: %d, SBW: %ld\n", sf, sbw);
    }
  }
  */
}