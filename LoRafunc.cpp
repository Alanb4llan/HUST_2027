#include "LoRafunc.h"
#include <Arduino.h>
#include "global.h"

// LoRa transmission timing
unsigned long lastLoRaSend = 0;
const unsigned long LoRaSendInterval = 1000; // Send every 1 second (adjust as needed)

// Packet counter for tracking
uint16_t packetCounter = 0;

// ==================================================================================
// DATA STRUCTURES FOR EFFICIENT TRANSMISSION
// ==================================================================================

// Structure 1: Critical Vehicle Data (Priority 1)
struct CriticalData {
  float velocity;          // km/h
  float packVoltage;       // V
  float packCurrent;       // A
  float motorCurrent;      // A
  uint8_t flags;           // Bit flags for errors/warnings
  uint16_t counter;        // Packet counter
} __attribute__((packed));

// Structure 2: Battery Data (Priority 2)
struct BatteryData {
  float lowCellVoltage;    // V
  float highCellVoltage;   // V
  float avgCellVoltage;    // V
  uint8_t cellHighTemp;    // °C
  uint8_t cellLowTemp;     // °C
  uint8_t cellAvgTemp;     // °C
  uint8_t bmsInternalTemp; // °C
  uint16_t counter;        // Packet counter
} __attribute__((packed));

// Structure 3: Motor & Thermal Data (Priority 3)
struct MotorThermalData {
  float motorTemp;         // °C
  float heatSinkTemp;      // °C
  float distance;          // km
  uint16_t counter;        // Packet counter
} __attribute__((packed));

// Structure 4: MPPT Data (Priority 4)
struct MPPTData {
  float mppt1Power;        // W
  float mppt2Power;        // W
  float mppt3Power;        // W
  float totalPower;        // W
  uint16_t counter;        // Packet counter
} __attribute__((packed));

// ==================================================================================
// LORA INITIALIZATION
// ==================================================================================

float sendInterval = 1.0;     // seconds between sends (used by sender)
int   sf           = 7;       // spreading factor
long  sbw          = 125000;  // bandwidth: 125 kHz

void setupLoRa() {
  Serial.println("Initializing LoRa radio...");

  LoRa.setSPI(SPI);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);

  while (!LoRa.begin(868E6)) {
    Serial.println("LoRa begin failed, retrying...");
    delay(500);
  }

  // Configure LoRa parameters
  LoRa.setSpreadingFactor(sf);
  LoRa.setSignalBandwidth(sbw);
  LoRa.setSyncWord(0xF3);           // Private network sync word
  LoRa.enableCrc();                  // Enable CRC for error detection
  LoRa.setTxPower(20);              // Max power for better range

  Serial.println("LoRa initialized OK");
  Serial.print("Frequency: 868 MHz | SF: ");
  Serial.print(sf);
  Serial.print(" | BW: ");
  Serial.print(sbw / 1000);
  Serial.println(" kHz");
}

// ==================================================================================
// SEND CRITICAL DATA PACKET (Priority 1)
// ==================================================================================

void sendCriticalData() {
  CriticalData data;
  
  // Pack critical telemetry
  data.velocity = VehicleVelocity;
  data.packVoltage = (float)PackVoltage;
  data.packCurrent = (float)PackCurrent;
  data.motorCurrent = MotorCurrent;
  data.counter = packetCounter;
  
  // Create error/status flags byte
  data.flags = 0;
  if (MCerror)    data.flags |= (1 << 0);  // Bit 0: Motor Controller Error
  if (BMSerror)   data.flags |= (1 << 1);  // Bit 1: BMS Error
  if (HighTemp)   data.flags |= (1 << 2);  // Bit 2: High Temperature Warning
  if (Left_Turn)  data.flags |= (1 << 3);  // Bit 3: Left Turn Signal
  if (Right_Turn) data.flags |= (1 << 4);  // Bit 4: Right Turn Signal
  if (Hazard)     data.flags |= (1 << 5);  // Bit 5: Hazard Lights
  if (CCactive)   data.flags |= (1 << 6);  // Bit 6: Cruise Control Active
  
  // Send packet
  LoRa.beginPacket();
  LoRa.write(0x01); // Packet type identifier: Critical Data
  LoRa.write((uint8_t*)&data, sizeof(data));
  LoRa.endPacket();
  
  Serial.print("LoRa TX [CRITICAL]: Speed=");
  Serial.print(data.velocity, 1);
  Serial.print(" km/h, Pack=");
  Serial.print(data.packVoltage, 1);
  Serial.print("V/");
  Serial.print(data.packCurrent, 1);
  Serial.print("A, Flags=0b");
  Serial.println(data.flags, BIN);
}

// ==================================================================================
// SEND BATTERY DATA PACKET (Priority 2)
// ==================================================================================

void sendBatteryData() {
  BatteryData data;
  
  data.lowCellVoltage = (float)LowCellVoltage;
  data.highCellVoltage = (float)HighCellVoltage;
  data.avgCellVoltage = (float)AverageCellVoltage;
  data.cellHighTemp = CellHighTemperature;
  data.cellLowTemp = CellLowTemperature;
  data.cellAvgTemp = CellAverageTemperature;
  data.bmsInternalTemp = InternalTempBMS;
  data.counter = packetCounter;
  
  LoRa.beginPacket();
  LoRa.write(0x02); // Packet type identifier: Battery Data
  LoRa.write((uint8_t*)&data, sizeof(data));
  LoRa.endPacket();
  
  Serial.print("LoRa TX [BATTERY]: Cells=");
  Serial.print(data.lowCellVoltage, 4);
  Serial.print("-");
  Serial.print(data.highCellVoltage, 4);
  Serial.print("V, Temps=");
  Serial.print(data.cellLowTemp);
  Serial.print("-");
  Serial.print(data.cellHighTemp);
  Serial.println("°C");
}

// ==================================================================================
// SEND MOTOR/THERMAL DATA PACKET (Priority 3)
// ==================================================================================

void sendMotorThermalData() {
  MotorThermalData data;
  
  data.motorTemp = MotorTemp;
  data.heatSinkTemp = HeatSinkTemp;
  data.distance = Distance;
  data.counter = packetCounter;
  
  LoRa.beginPacket();
  LoRa.write(0x03); // Packet type identifier: Motor/Thermal Data
  LoRa.write((uint8_t*)&data, sizeof(data));
  LoRa.endPacket();
  
  Serial.print("LoRa TX [MOTOR]: Temp=");
  Serial.print(data.motorTemp, 1);
  Serial.print("°C, MC Temp=");
  Serial.print(data.heatSinkTemp, 1);
  Serial.print("°C, Dist=");
  Serial.print(data.distance, 2);
  Serial.println("km");
}

// ==================================================================================
// SEND MPPT DATA PACKET (Priority 4)
// ==================================================================================

void sendMPPTData() {
  MPPTData data;
  
  data.mppt1Power = (float)MPPTOutputPower1;
  data.mppt2Power = (float)MPPTOutputPower2;
  data.mppt3Power = (float)MPPTOutputPower3;
  data.totalPower = (float)TotMPPT;
  data.counter = packetCounter;
  
  LoRa.beginPacket();
  LoRa.write(0x04); // Packet type identifier: MPPT Data
  LoRa.write((uint8_t*)&data, sizeof(data));
  LoRa.endPacket();
  
  Serial.print("LoRa TX [MPPT]: Total=");
  Serial.print(data.totalPower, 2);
  Serial.print("W (");
  Serial.print(data.mppt1Power, 1);
  Serial.print("/");
  Serial.print(data.mppt2Power, 1);
  Serial.print("/");
  Serial.print(data.mppt3Power, 1);
  Serial.println(")");
}

// ==================================================================================
// MAIN LORA TRANSMISSION HANDLER
// ==================================================================================
// Call this from loop() to handle periodic LoRa transmissions
// Sends all data packets in sequence with small delays between them

void handleLoRaTransmission() {
  unsigned long currentMillis = millis();
  
  // Check if it's time to send
  if (currentMillis - lastLoRaSend >= LoRaSendInterval) {
    
    Serial.println("--- LoRa Transmission Cycle ---");
    
    // Send all packet types with small delays
    sendCriticalData();
    delay(50); // Small delay between packets
    
    sendBatteryData();
    delay(50);
    
    sendMotorThermalData();
    delay(50);
    
    sendMPPTData();
    delay(50);
    
    // Increment packet counter
    packetCounter++;
    
    Serial.print("Packet cycle #");
    Serial.print(packetCounter);
    Serial.println(" complete");
    Serial.println("-------------------------------");
    
    lastLoRaSend = currentMillis;
  }
}

// ==================================================================================
// ALTERNATIVE: SEND SINGLE CONSOLIDATED PACKET
// ==================================================================================
// Use this instead of separate packets if you want all data in one transmission
// Comment out handleLoRaTransmission() and use this instead

void sendConsolidatedPacket() {
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastLoRaSend >= LoRaSendInterval) {
    
    LoRa.beginPacket();
    LoRa.write(0xFF); // Packet type: Consolidated
    
    // Critical data
    LoRa.write((uint8_t*)&VehicleVelocity, sizeof(float));
    LoRa.write((uint8_t*)&PackVoltage, sizeof(double));
    LoRa.write((uint8_t*)&PackCurrent, sizeof(double));
    LoRa.write((uint8_t*)&MotorCurrent, sizeof(float));
    
    // Battery cells
    LoRa.write((uint8_t*)&LowCellVoltage, sizeof(double));
    LoRa.write((uint8_t*)&HighCellVoltage, sizeof(double));
    
    // Temperatures
    LoRa.write(InternalTempBMS);
    LoRa.write(CellHighTemperature);
    LoRa.write(CellLowTemperature);
    
    // MPPT
    LoRa.write((uint8_t*)&TotMPPT, sizeof(double));
    
    // Flags
    uint8_t flags = 0;
    if (MCerror) flags |= (1 << 0);
    if (BMSerror) flags |= (1 << 1);
    LoRa.write(flags);
    
    // Counter
    LoRa.write((uint8_t*)&packetCounter, sizeof(uint16_t));
    
    LoRa.endPacket();
    
    packetCounter++;
    lastLoRaSend = currentMillis;
    
    Serial.print("LoRa TX [CONSOLIDATED] Packet #");
    Serial.println(packetCounter);
  }
}

// ==================================================================================
// TEST FUNCTION: Send simple heartbeat
// ==================================================================================

void sendLoRaHeartbeat() {
  String msg = "SOLAR_CAR_OK_" + String(millis());
  
  LoRa.beginPacket();
  LoRa.print(msg);
  LoRa.endPacket();
  
  Serial.print("LoRa Heartbeat: ");
  Serial.println(msg);
}
