#include <STM32_CAN.h>
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

 * * ==================================================================================*/
float MotorCurrent, MotorVoltage, VehicleVelocity, MotorRPM, Amps, Distance, HeatSinkTemp, MotorTemp;
uint8_t InternalTempBMS, CellHighTemperature, CellLowTemperature, CellAverageTemperature, CellHighTemperature_ID, CellLowTemperature_ID;
double PackCurrent, PackVoltage, LowCellVoltage, HighCellVoltage, AverageCellVoltage;
double MPPTOutputPower1, MPPTOutputPower2, MPPTOutputPower3, TotMPPT;
float TargetRPM, TargetCurrent, Brake;
bool Left_Turn, Right_Turn, Hazard, CCactive, MCerror, HighTemp, BMSerror; 
unsigned long prevmsg = 0;


// Using CAN1 onpins (PB8/PB9)
STM32_CAN Can(PB8, PB9); 
static CAN_message_t rxMsg;
static CAN_message_t txMsg;

void setup() {
  Serial.begin(115200);
  
  Can.begin();
  Can.setBaudRate(500000); // 500kbps

//-----------------Filters--------------------------//

  Can.setAutoBusOffRecovery(true); // Recover from EMI/Noise
  Can.setIRQPriority(5, 0);        // Higher priority than standard tasks
  
  // --- Hardware Filtering ---
  // Bank 0: Motor Controller (Allows 0x400 to 0x40F)
  Can.setFilterSingleMask(0, 0x400, 0x7F0, STD); 
  
  // Bank 1: BMS (Allows 0x600 to 0x607)
  Can.setFilterSingleMask(1, 0x600, 0x7F8, STD);
  
  // Bank 2: MPPTs (Allows 0x200 to 0x23F)  
  Can.setFilterSingleMask(2, 0x200, 0x7C0, STD);

//-----------------Filters--------------------------//
  
  Serial.println("STM32 Solar Car Controller Initialized");

    
  pinMode(PA10, OUTPUT); 
  pinMode(PA8, OUTPUT); //RIGHT INDICATOR
  pinMode(PA9, OUTPUT); //LEFT INDICATOR
}

void loop() {

  CanReadAll();

  if (millis() - prevmsg > 100) {
    printTelemetryToSerial();
    prevmsg = millis();
  }

  
  digitalWrite(PA10, HIGH); //Brake lights
  digitalWrite(PA8, HIGH); //RIGHT INDICATOR
  digitalWrite(PA9, HIGH); //LEFT INDICATOR
  

}