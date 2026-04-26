#include "global.h"

// ==================================================================================
// GLOBAL VARIABLE DEFINITIONS
// This is the single file where all shared variables are actually allocated.
// Every other file sees them via the extern declarations in global.h.
// ==================================================================================

// --- CAN Objects
STM32_CAN Can(PB8, PB9);
CAN_message_t rxMsg;
CAN_message_t txMsg;

// --- Motor Controller
float MotorCurrent    = 0;
float MotorVoltage    = 0;
float VehicleVelocity = 0;
float MotorRPM        = 0;
float Amps            = 0;
float Distance        = 0;
float HeatSinkTemp    = 0;
float MotorTemp       = 0;

// --- Drive Control 
float TargetRPM     = 0;
float TargetCurrent = 0;
float Brake         = 0;

// --- BMS Temperatures
uint8_t InternalTempBMS        = 0;
uint8_t CellHighTemperature    = 0;
uint8_t CellLowTemperature     = 0;
uint8_t CellAverageTemperature = 0;
uint8_t CellHighTemperature_ID = 0;
uint8_t CellLowTemperature_ID  = 0;

// --- BMS Pack Data 
double PackCurrent      = 0;
double PackVoltage      = 0;
double LowCellVoltage   = 0;
double HighCellVoltage  = 0;
double AverageCellVoltage = 0;

// --- MPPT Power 
double MPPTOutputPower1 = 0;
double MPPTOutputPower2 = 0;
double MPPTOutputPower3 = 0;
double TotMPPT          = 0;

// --- Status
bool Left_Turn  = false;
bool Right_Turn = false;
bool Hazard     = false;
bool CCactive   = false;
bool MCerror    = false;
bool HighTemp   = false;
bool BMSerror   = false;

//Timing
unsigned long prevmsg = 0;

// --- LoRa Settings 
float sendInterval = 1.0;   // seconds between sends
int   sf           = 7;     // spreading factor
long  sbw          = 125000; // bandwidth: 125 kHz

// --- LoRa Internal State
unsigned long lastLoRaSend = 0;
uint16_t      packetCounter = 0;
