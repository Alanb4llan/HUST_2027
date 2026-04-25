#include "STM32_CAN.h"

/* * ==================================================================================
 * CAN BUS TOPOLOGY & IDENTIFIER MAP
 * ==================================================================================
 * * --- 1. TRANSMITTED BY THIS STM32 (CONTROL) ---
 * ID 0x501 (1281) | Motor Controller
 * ID 0x176 (374)  | Dashboard/Lights
 * * --- 2. RECEIVED FROM MOTOR CONTROLLER (TRITON/WAVESCULPT) ---
 * ID 0x401 (1025) | MC Status 
 * ID 0x402 (1026) | Motor Bus Data
 * ID 0x403 (1027) | Velocity/RPM
 * ID 0x40B (1035) | Temperatures
 * ID 0x40E (1038) | Odometer/Ah
 * * --- 3. RECEIVED FROM BMS (ORION BMS STYLE) ---
 * ID 0x601 (1537) | BMS Temps
 * ID 0x602 (1538) | Pack Data
 * ID 0x603 (1539) | Cell Voltages
 * ID 0x605 (1541) | BMS Status
 * * --- 4. RECEIVED FROM MPPTS (DILITHIUM/CUSTOM) ---
 * ID 0x200 (512)  | MPPT 1
 * ID 0x210 (528)  | MPPT 2
 * ID 0x220 (544)  | MPPT 3

 * * ==================================================================================
 */
 
/*


//Sends Control signals (RPM and Current) to the Motor Controller

void sendDriveCAN(float value1, float value2) {
  txMsg.id = 0x501;
  txMsg.len = 8;
  txMsg.flags.extended = 0;
  
  // Pack floats into bytes
  memcpy(&txMsg.buf[0], &value1, 4);
  memcpy(&txMsg.buf[4], &value2, 4);
  
  Can.write(txMsg);
}

//Sends Dashboard/Signal data (Blinkers, Hazard, Brake)
void sendDashboardCAN() {
  txMsg.id = 0x176;
  txMsg.len = 8;
  txMsg.flags.extended = 0;
  
  // Clear the buffer to ensure no "ghost" data
  memset(txMsg.buf, 0, 8);

  if(Left_Turn)  txMsg.buf[0] = 1;
  if(Right_Turn) txMsg.buf[1] = 1;
  if(Hazard)     txMsg.buf[2] = 1;
  if(Brake != 0) txMsg.buf[3] = 1;

  Can.write(txMsg);
}

/**
 * Reads and decodes all messages currently in the STM32 RX buffer
 */
void CanReadAll() {
  // Loop through all messages waiting in the hardware FIFO
  while (Can.read(rxMsg)) {
    switch (rxMsg.id) {
      case 0x401: 
        MCerror = (rxMsg.buf[2] != 0); 
        break;

      case 0x402: // Motor Bus Data   
        //MotorVoltage = *((float*)(rxMsg.buf));     // add if neccesseary
        MotorCurrent = *((float*)(rxMsg.buf + 4)); 
        break;

      case 0x403: // Velocity
        //MotorRPM = *((float*)(rxMsg.buf));         // add if neccesseary
        VehicleVelocity = *((float*)(rxMsg.buf + 4)) * 3.6; 
        break;

      case 0x40B: // Temperatur Measurements
        HeatSinkTemp = *((float*)(rxMsg.buf+4));
        MotorTemp = *((float*)(rxMsg.buf));
        break;

      case 0x40E: // Odometer & Bus AmpHours Measurement
      Distance = *((float*)(rxMsg.buf)); // Distance travelled since start
      break;

      case 0x601: // BMS Temperatures & IDs
        InternalTempBMS = rxMsg.buf[1];
        CellHighTemperature = rxMsg.buf[2];
        CellLowTemperature = rxMsg.buf[3];
        CellAverageTemperature = rxMsg.buf[4];
        CellHighTemperature_ID = rxMsg.buf[5];
        CellLowTemperature_ID = rxMsg.buf[6];
      break; 

      case 0x602: // Pack Data (Spänning & Ström)
        if (rxMsg.buf[0] >= 128) {
          PackCurrent = ((double)((rxMsg.buf[0] - 256) * 256 + rxMsg.buf[1])) / 10.0;
        } else {
          PackCurrent = ((double)(rxMsg.buf[0] * 256 + rxMsg.buf[1])) / 10.0;
        }
        PackVoltage = ((double)(rxMsg.buf[2] * 256 + rxMsg.buf[3])) / 10.0;
        LowCellVoltage = ((double)(rxMsg.buf[4] * 256 + rxMsg.buf[5])) / 10000.0;
        HighCellVoltage = ((double)(rxMsg.buf[6] * 256 + rxMsg.buf[7])) / 10000.0;
        
        break;  

      case 0x603: // Snittspänning celler
        AverageCellVoltage = ((double)(rxMsg.buf[0] * 256 + rxMsg.buf[1])) / 10000.0;
        break;

      case 0x605: // BMS Error flags
        BMSerror = (rxMsg.buf[6] != 0 || rxMsg.buf[7] != 0);
        break;

      case 0x200: case 0x210: case 0x220:
        processMPPT(rxMsg);
        break;
    }
  }
  TotMPPT = MPPTOutputPower1 + MPPTOutputPower2 + MPPTOutputPower3;
}

// Helper to handle MPPT logic
void processMPPT(CAN_message_t &m) {
  double outV = ((double)(m.buf[4] * 256 + m.buf[5])) / 100.0;
  double outI;
  if (m.buf[6] >= 128) {
    outI = ((double)((m.buf[6] - 256) * 256 + m.buf[7])) * 0.0005;
  } else {
    outI = ((double)(m.buf[6] * 256 + m.buf[7])) * 0.0005;
  }

  if (m.id == 0x200) MPPTOutputPower1 = outV * outI;
  else if (m.id == 0x210) MPPTOutputPower2 = outV * outI;
  else if (m.id == 0x220) MPPTOutputPower3 = outV * outI;
}



void printTelemetryToSerial() {
  Serial.println("--- VEHICLE STATUS ---");
  
  Serial.print("Speed: "); Serial.print(VehicleVelocity, 2);
  Serial.print(" km/h | Dist: "); Serial.print(Distance, 2);
  Serial.print(" km | Total MPPT: "); Serial.print(TotMPPT, 2);
  Serial.println(" W");

  Serial.print("Battery: "); Serial.print(PackVoltage, 2);
  Serial.print(" V | "); Serial.print(PackCurrent, 2);
  Serial.print(" A | BMS Temp: "); Serial.print(InternalTempBMS);
  Serial.println(" C");

  Serial.print("Cells: Low: "); Serial.print(LowCellVoltage, 4);
  Serial.print(" V | High: "); Serial.print(HighCellVoltage, 4);
  Serial.print(" V | Avg: "); Serial.print(AverageCellVoltage, 4);
  Serial.println(" V");

  Serial.print("Cell Temps: Low: "); Serial.print(CellLowTemperature);
  Serial.print(" C (ID:"); Serial.print(CellLowTemperature_ID);
  Serial.print(") | High: "); Serial.print(CellHighTemperature);
  Serial.print(" C (ID:"); Serial.print(CellHighTemperature_ID);
  Serial.print(") | Avg: "); Serial.print(CellAverageTemperature);
  Serial.println(" C");

  Serial.print("Motor: "); Serial.print(MotorCurrent, 2);
  Serial.print(" A | Motor Temp: "); Serial.print(MotorTemp, 2);
  Serial.print(" C | MC Temp: "); Serial.print(HeatSinkTemp, 2);
  Serial.println(" C");

  Serial.print("MPPTs: P1: "); Serial.print(MPPTOutputPower1, 2);
  Serial.print(" | P2: "); Serial.print(MPPTOutputPower2, 2);
  Serial.print(" | P3: "); Serial.print(MPPTOutputPower3, 2);
  Serial.println();

  Serial.println("----------------------");
}
