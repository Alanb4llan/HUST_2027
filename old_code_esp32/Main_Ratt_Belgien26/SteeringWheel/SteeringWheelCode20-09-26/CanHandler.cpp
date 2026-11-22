#include "CanHandler.h"
#include "Globals.h"
#include "CruiseControl.h"
#include <ESP32-TWAI-CAN.hpp>
#include "driver/twai.h"

CanFrame msg;

void InitCAN() {
  ESP32Can.setPins(CAN_TX, CAN_RX);
  ESP32Can.setRxQueueSize(10);
  ESP32Can.setTxQueueSize(10);
  
  if (ESP32Can.begin(ESP32Can.convertSpeed(500), CAN_TX, CAN_RX, 10, 10)) {
    Serial.println("CAN bus speed 500 started!");
  }
}

void ProcessDrivingCAN() {
  if (millis() - prevmsg > 100) { 
    ProcessCruiseControl(); 
    sendDriveCAN(inputs.TargetRPM, inputs.TargetCurrent);
    sendESPCAN();
    prevmsg = millis(); 
    twai_status_info_t status; 
    twai_get_status_info(&status);
  }
  CanReadAll(); 
}

void CanReadAll() {
  if (ESP32Can.readFrame(msg, 0)) {
    switch (msg.identifier) {
      case CAN_ID_MC_ERROR:
        motor.MCerror = (msg.data[2] != 0);
        break;
      case CAN_ID_MC_BUS: 
        motor.Current = *((float*)(msg.data+4));  
        motor.Voltage = *((float*)(msg.data));    
        break;
      case CAN_ID_MC_VEL: 
        motor.VehicleVelocity = *((float*)(msg.data + 4)) * 3.6; 
        motor.RPM = *((float*)(msg.data));
        break;
      case CAN_ID_MC_TEMP: 
        motor.HeatSinkTemp = *((float*)(msg.data+4));
        motor.MotorTemp = *((float*)(msg.data));
        break;
      case CAN_ID_MC_ODO: 
        motor.Amps = *((float*)(msg.data+4)); 
        motor.Distance = *((float*)(msg.data)); 
        break;
      case CAN_ID_BMS_TEMP: 
        bms.InternalTemp = msg.data[1];
        bms.CellHighTemp = msg.data[2];
        bms.CellLowTemp = msg.data[3];
        bms.CellAverageTemp = msg.data[4];
        bms.HighTemp = (msg.data[1] >= 50 || msg.data[2] >= 50);
        break;
      case CAN_ID_BMS_PACK: {
        int16_t raw_current = (msg.data[0] << 8) | msg.data[1];
        bms.PackCurrent = raw_current / 10.0;
        
        uint16_t raw_voltage = (msg.data[2] << 8) | msg.data[3];
        bms.PackVoltage = raw_voltage / 10.0;
        
        uint16_t raw_low = (msg.data[4] << 8) | msg.data[5];
        bms.LowCellVoltage = raw_low / 10000.0;
        
        uint16_t raw_high = (msg.data[6] << 8) | msg.data[7];
        bms.HighCellVoltage = raw_high / 10000.0;
        break;
      }
      case CAN_ID_BMS_CELL:
        bms.AverageCellVoltage = ((msg.data[0] << 8) | msg.data[1]) / 10000.0;
        break;
      case CAN_ID_BMS_ERROR:
        bms.BMSerror = (msg.data[6] != 0 || msg.data[7] != 0);
        break;
      case CAN_ID_ESP_RX: 
        if(msg.data[0] != 0) { state.CCactive = false; }
        state.SafeState = (msg.data[1] != 0);
        break;
      case CAN_ID_MPPT1:
      case CAN_ID_MPPT2:
      case CAN_ID_MPPT3:
      case CAN_ID_MPPT4: {
        int mppt_idx = (msg.identifier - 0x200) / 0x10; // Maps 0x200->0, 0x210->1, etc.
        mppt[mppt_idx].InputVoltage = ((msg.data[0] << 8) | msg.data[1]) / 100.0;
        mppt[mppt_idx].InputCurrent = (int16_t)((msg.data[2] << 8) | msg.data[3]) * 0.0005;
        mppt[mppt_idx].OutputVoltage = ((msg.data[4] << 8) | msg.data[5]) / 100.0;
        mppt[mppt_idx].OutputCurrent = (int16_t)((msg.data[6] << 8) | msg.data[7]) * 0.0005;
        mppt[mppt_idx].OutputPower = mppt[mppt_idx].OutputVoltage * mppt[mppt_idx].OutputCurrent;
        break;
      }
    }
    TotMPPT = mppt[0].OutputPower + mppt[1].OutputPower + mppt[2].OutputPower + mppt[3].OutputPower;
  }
}

void sendDriveCAN(float value1, float value2) {
  uint8_t data[8]; 
  memcpy(data, &value1, sizeof(float));       
  memcpy(data + 4, &value2, sizeof(float));   
  
  twai_message_t msg1 = {0};
  msg1.identifier = CAN_ID_DRIVE_CMD;                    
  msg1.extd = 0;                               
  msg1.data_length_code = 8;                   
  memcpy(msg1.data, data, 8);
  
  ESP32Can.writeFrame(msg1);
}

void sendESPCAN() {
  uint8_t data[8] = {0};
  if (state.Left_Turn) data[0] = 1; 
  else if (state.Right_Turn) data[1] = 1; 
  else if (state.Hazard) data[2] = 1;
  
  if (inputs.Brake != 0) data[3] = 1;
  
  twai_message_t msg1 = {0};
  msg1.identifier = CAN_ID_ESP_TX; 
  msg1.extd = 0;                               
  msg1.data_length_code = 8;                   
  memcpy(msg1.data, data, 8);

  ESP32Can.writeFrame(msg1);
}