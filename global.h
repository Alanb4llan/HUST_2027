#ifndef GLOBAL_H
#define GLOBAL_H

#include "STM32_CAN.h"
#include <Arduino.h>

// ==================================================================================
// GLOBAL VARIABLE DECLARATIONS
// Definitions live in HUST27.ino — these extern declarations make them
// visible to all other .cpp / .ino files that include this header.
// ==================================================================================

// --- CAN objects ---
extern STM32_CAN Can;
extern CAN_message_t rxMsg;
extern CAN_message_t txMsg;

// --- Motor Controller ---
extern float  MotorCurrent;
extern float  MotorVoltage;
extern float  VehicleVelocity;
extern float  MotorRPM;
extern float  Amps;
extern float  Distance;
extern float  HeatSinkTemp;
extern float  MotorTemp;

// --- Drive Control ---
extern float  TargetRPM;
extern float  TargetCurrent;
extern float  Brake;

// --- BMS Temperatures ---
extern uint8_t InternalTempBMS;
extern uint8_t CellHighTemperature;
extern uint8_t CellLowTemperature;
extern uint8_t CellAverageTemperature;
extern uint8_t CellHighTemperature_ID;
extern uint8_t CellLowTemperature_ID;

// --- BMS Pack Data ---
extern double PackCurrent;
extern double PackVoltage;
extern double LowCellVoltage;
extern double HighCellVoltage;
extern double AverageCellVoltage;

// --- MPPT Power ---
extern double MPPTOutputPower1;
extern double MPPTOutputPower2;
extern double MPPTOutputPower3;
extern double TotMPPT;

// --- Status / Control Flags ---
extern bool Left_Turn;
extern bool Right_Turn;
extern bool Hazard;
extern bool CCactive;
extern bool MCerror;
extern bool HighTemp;
extern bool BMSerror;

// --- Timing ---
extern unsigned long prevmsg;

// --- LoRa Settings ---
extern float sendInterval;
extern int   sf;
extern long  sbw;
 
// --- LoRa Internal State ---
extern unsigned long lastLoRaSend;
extern uint16_t      packetCounter;

#endif
