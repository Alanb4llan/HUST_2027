#ifndef CAN_HANDLER_H
#define CAN_HANDLER_H
#include <Arduino.h>

void InitCAN();
void ProcessDrivingCAN();
void CanReadAll();
void sendDriveCAN(float value1, float value2);
void sendESPCAN();

#endif