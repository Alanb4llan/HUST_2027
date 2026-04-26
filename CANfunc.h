#ifndef CANFUNC_H
#define CANFUNC_H

#include "STM32_CAN.h"
#include <Arduino.h>
#include "global.h"


void sendDriveCAN(float value1, float value2);
void sendDashboardCAN();
void CanReadAll();
void processMPPT(CAN_message_t &m);
void printTelemetryToSerial();

#endif