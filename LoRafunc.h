#ifndef LORAFUNC_H
#define LORAFUNC_H

#include <LoRa.h>
#include <SPI.h>
#include <Arduino.h>
#include "global.h"

// Pins for Nucleo-L4R6G + RFM95W
// NSS=D10, SCK=D13, MISO=D12, MOSI=D11, RST=D9, DIO0=D2

#define LORA_SS   PC0   // NSS (Chip Select)
#define LORA_RST  PC7    // Reset
#define LORA_DIO0 PA10    // DIO0 (interrupt)
#define LORA_SCK  PA5
#define LORA_MISO PA6
#define LORA_MOSI PA7

// ==================================================================================
// DATA STRUCTURES FOR EFFICIENT TRANSMISSION
// ==================================================================================

// Structure 1: Critical Vehicle Data (Priority 1)
struct CriticalData {
  float velocity;          // km/h
  float packVoltage;       // V
  float packCurrent;       // A
  float motorCurrent;      // A
  uint8_t flags;           // Bit flags for errors/warnings
  uint16_t counter;        // Packet counter
} __attribute__((packed));

// Structure 2: Battery Data (Priority 2)
struct BatteryData {
  float lowCellVoltage;    // V
  float highCellVoltage;   // V
  float avgCellVoltage;    // V
  uint8_t cellHighTemp;    // °C
  uint8_t cellLowTemp;     // °C
  uint8_t cellAvgTemp;     // °C
  uint8_t bmsInternalTemp; // °C
  uint16_t counter;        // Packet counter
} __attribute__((packed));

// Structure 3: Motor & Thermal Data (Priority 3)
struct MotorThermalData {
  float motorTemp;         // °C
  float heatSinkTemp;      // °C
  float distance;          // km
  uint16_t counter;        // Packet counter
} __attribute__((packed));

// Structure 4: MPPT Data (Priority 4)
struct MPPTData {
  float mppt1Power;        // W
  float mppt2Power;        // W
  float mppt3Power;        // W
  float totalPower;        // W
  uint16_t counter;        // Packet counter
} __attribute__((packed));

extern float sendInterval;
extern int sf;
extern long sbw;

void setupLoRa();
void sendLoRaTestMessage();  
void receiveLoRaMessage(); 
void sendConsolidatedPacket();

#endif