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

extern float sendInterval;
extern int sf;
extern long sbw;

void setupLoRa();
void sendLoRaTestMessage();  
void receiveLoRaMessage(); 
void sendConsolidatedPacket();

#endif