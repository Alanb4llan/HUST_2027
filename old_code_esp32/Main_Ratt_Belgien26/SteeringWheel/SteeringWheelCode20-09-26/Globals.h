#ifndef GLOBALS_H
#define GLOBALS_H
#include <Arduino.h>

// Pins
constexpr uint8_t GAS_POTENTIOMETER = 16;
constexpr uint8_t BRAKE_POTENTIOMETER = 15;
constexpr uint8_t LEFT_TURN_BUTTON = 7;
constexpr uint8_t RIGHT_TURN_BUTTON = 6;
constexpr uint8_t HAZARD_BUTTON = 1;
constexpr uint8_t OK_GEAR_BUTTON = 2;
constexpr uint8_t CC_UP_BUTTON = 17;
constexpr uint8_t CC_DOWN_BUTTON = 8;
constexpr uint8_t DRIVE_SELECT_BUTTON = 9;
constexpr uint8_t CAN_TX = 4;
constexpr uint8_t CAN_RX = 5;

// CAN IDs
constexpr uint32_t CAN_ID_MC_ERROR  = 0x401;
constexpr uint32_t CAN_ID_MC_BUS    = 0x402;
constexpr uint32_t CAN_ID_MC_VEL    = 0x403;
constexpr uint32_t CAN_ID_MC_TEMP   = 0x40B;
constexpr uint32_t CAN_ID_MC_ODO    = 0x40E;
constexpr uint32_t CAN_ID_BMS_TEMP  = 0x601;
constexpr uint32_t CAN_ID_BMS_PACK  = 0x602;
constexpr uint32_t CAN_ID_BMS_CELL  = 0x603;
constexpr uint32_t CAN_ID_BMS_ERROR = 0x605;
constexpr uint32_t CAN_ID_MPPT1     = 0x200;
constexpr uint32_t CAN_ID_MPPT2     = 0x210;
constexpr uint32_t CAN_ID_MPPT3     = 0x220;
constexpr uint32_t CAN_ID_MPPT4     = 0x230;
constexpr uint32_t CAN_ID_ESP_RX    = 0x175;
constexpr uint32_t CAN_ID_ESP_TX    = 0x176;
constexpr uint32_t CAN_ID_DRIVE_CMD = 0x501;

// Telemetry Structures
struct MotorData {
  float Current;
  float Voltage;
  float VehicleVelocity;
  float RPM;
  float HeatSinkTemp;
  float MotorTemp;
  float Amps;
  float Distance;
  bool MCerror;
};

struct BmsData {
  uint8_t InternalTemp;
  uint8_t CellHighTemp;
  uint8_t CellLowTemp;
  uint8_t CellAverageTemp;
  double PackCurrent;
  double PackVoltage;
  double LowCellVoltage;
  double HighCellVoltage;
  double AverageCellVoltage;
  bool BMSerror;
  bool HighTemp;
};

struct MpptData {
  double InputVoltage;
  double InputCurrent;
  double OutputVoltage;
  double OutputCurrent;
  double OutputPower;
};

struct VehicleInputs {
  float Gas;
  float MaxGas;
  float MinGas;
  float Brake;
  float MaxBrake;
  float MinBrake;
  float TargetRPM;
  float TargetCurrent;
  int GasLimiter;
  int CCSpeed;
};

struct VehicleState {
  bool Left_Turn;
  bool Right_Turn;
  bool Hazard;
  bool DriveButton;
  bool SafeState;
  bool InStartScreen;
  bool CCactive;
};

// Shared Globals
extern MotorData motor;
extern BmsData bms;
extern MpptData mppt[4];
extern double TotMPPT;
extern VehicleInputs inputs;
extern VehicleState state;

extern unsigned long prevmsg;

// ISR Flags
extern volatile bool flag_LeftTurn;
extern volatile bool flag_RightTurn;
extern volatile bool flag_Hazard;
extern volatile bool flag_CCUp;
extern volatile bool flag_CCDown;
extern volatile bool flag_Gear;
extern volatile bool flag_DriveSelect;

#endif