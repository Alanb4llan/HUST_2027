#ifndef CAN_FUNCTIONS_H
#define CAN_FUNCTIONS_H

#include <ESP32-TWAI-CAN.hpp>

// Define pins for CAN tranceiver
#define CAN_TX	5
#define CAN_RX	4

// Define variables for CAN-data transmission
extern float battery_volt;
extern float battery_current;
extern float battery_cell_LOW_volt;
extern float battery_cell_HIGH_volt;
extern float battery_cell_AVG_volt;
extern float battery_cell_LOW_temp;
extern float battery_cell_HIGH_temp;
extern float battery_cell_AVG_temp;
extern float battery_cell_ID_HIGH_volt;
extern float battery_cell_ID_LOW_volt;
extern float BMS_temp;
extern float BATTERY_WATTHOURS_SINCE_START;

extern float velocity;
extern float distance_travelled;
extern float motor_current;
extern float motor_temp;
extern float motor_controller_temp;
extern float driverRPM;
extern float driver_current;



extern float MPPTInputPower1;
extern float MPPTInputPower2;
extern float MPPTInputPower3;
extern float MPPTInputPower4;

extern float MPPTOutputPower1;
extern float MPPTOutputPower2;
extern float MPPTOutputPower3;
extern float MPPTOutputPower4;
extern float MPPT_total_watt_out;


extern CanFrame msg;

void setupCAN();
void sendCAN2steeringWheel(bool brakeLightCondition,bool safeStateCondition);
void assignCAN2variable();

#endif