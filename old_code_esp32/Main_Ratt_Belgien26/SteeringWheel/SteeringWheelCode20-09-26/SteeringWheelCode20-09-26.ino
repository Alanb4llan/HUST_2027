#include "Platform.h"
#include "App_Common.h"
#include "DispFunctions.h"
#include <SPI.h>
#include "Globals.h"
#include "Inputs.h"
#include "CanHandler.h"
#include "CruiseControl.h"

Gpu_Hal_Context_t host, *phost;

// Globals Initialization
MotorData motor = {0};
BmsData bms = {0};
MpptData mppt[4] = {0};
double TotMPPT = 0;
VehicleInputs inputs = {0, 0, 5000, 0, 0, 5000, 20000, 0, 1, 0};
VehicleState state = {false, false, false, false, false, true, false};
unsigned long prevmsg = 0;

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  phost = &host;
  App_Common_Init(&host);

  InitCAN(); 
  PinSetup();
  
  inputs.Gas = analogRead(GAS_POTENTIOMETER);
  inputs.Brake = analogRead(BRAKE_POTENTIOMETER); 
  inputs.MinGas = inputs.Gas; inputs.MaxGas = inputs.Gas; 
  inputs.MinBrake = inputs.Brake; inputs.MaxBrake = inputs.Brake;
}

void loop() {
  // Inputs run as fast as possible, non-blocking
  ReadButtons();
  
  if (state.InStartScreen) {
    CalibratePot();
  } else {
    ReadPot();
    ProcessDrivingCAN(); 
  } 

  // Rate-Limit SPI Display to 10Hz to prevent starving the ESP32
  static unsigned long prevDisplay = 0;
  if (millis() - prevDisplay >= 100) {
    prevDisplay = millis();
    if (state.InStartScreen) {
      start_screen();
    } else {
      main_screen();
    }
  }
}

void start_screen() {
  char maxgas_char[20], mingas_char[20], maxbrake_char[20], minbrake_char[20];

  snprintf(maxgas_char, sizeof(maxgas_char), "Max:%d", (int)inputs.MaxGas);
  snprintf(mingas_char, sizeof(mingas_char), "Min:%d", (int)inputs.MinGas);
  snprintf(maxbrake_char, sizeof(maxbrake_char), "Max:%d", (int)inputs.MaxBrake);
  snprintf(minbrake_char, sizeof(minbrake_char), "Min:%d", (int)inputs.MinBrake);

  Start_Set_Display(phost);
  draw_rect(phost, 10, 60, 200, 100, 70, 200, 200);
  draw_rect(phost, 280, 60, 470, 100, 70, 200, 200);
  draw_rect(phost, 10, 130, 200, 170, 70, 200, 200);
  draw_rect(phost, 280, 130, 470, 170, 70, 200, 200);

  Write_Text(phost, 178, 0, 30, "HUST");
  Write_Text(phost, 360, 10, 25, "Gas");
  Write_Text(phost, 50, 10, 25, "Brake");
  Write_Text(phost, 10, 65, 25, maxbrake_char);
  Write_Text(phost, 10, 135, 25, minbrake_char);
  Write_Text(phost, 280, 65, 25, maxgas_char);
  Write_Text(phost, 280, 135, 25, mingas_char);
  Write_Text_Color(phost, 135, 215, 16, "SET GAS &  BRAKE", 255, 1, 1);
  Finish_Display(phost);
}

void main_screen() {
  Start_Set_Display(phost);

  char txt[24]; 

  snprintf(txt, sizeof(txt), "Gas: %.2f", inputs.Gas); Write_Text(phost, 0, 100, 20, txt);
  snprintf(txt, sizeof(txt), "Brake: %.2f", inputs.Brake); Write_Text(phost, 0, 110, 20, txt);
  snprintf(txt, sizeof(txt), "Current %.2f", inputs.TargetCurrent); Write_Text(phost, 0, 120, 20, txt);
  snprintf(txt, sizeof(txt), "RPM %.2f", inputs.TargetRPM); Write_Text(phost, 0, 130, 20, txt);
  snprintf(txt, sizeof(txt), "MinGas %.2f", inputs.MinGas); Write_Text(phost, 0, 160, 20, txt);
  snprintf(txt, sizeof(txt), "MaxGas %.2f", inputs.MaxGas); Write_Text(phost, 0, 170, 20, txt);
  snprintf(txt, sizeof(txt), "MinBrake %.2f", inputs.MinBrake); Write_Text(phost, 0, 180, 20, txt);
  snprintf(txt, sizeof(txt), "MaxBrake %.2f", inputs.MaxBrake); Write_Text(phost, 0, 190, 20, txt);

  insert_line(phost, 0, 150, 0, 80, 20);
  Write_Text(phost, 40, 0, 21, "Power");
  snprintf(txt, sizeof(txt), "Motor:%.1fW", -1 * motor.Current * motor.Voltage); Write_Text(phost, 10, 20, 20, txt);
  snprintf(txt, sizeof(txt), "Solar:%.1fW", TotMPPT); Write_Text(phost, 10, 30, 20, txt);
  snprintf(txt, sizeof(txt), "Battery:%.1fW", -1 * bms.PackCurrent * bms.PackVoltage); Write_Text(phost, 10, 40, 20, txt);

  insert_line(phost,150,300,0,80,20);
  Write_Text(phost,180, 0, 21, "Voltages");
  snprintf(txt, sizeof(txt), "High: %.3fV", bms.HighCellVoltage); Write_Text(phost, 170, 20, 20, txt);
  snprintf(txt, sizeof(txt), "Avg: %.3fV", bms.AverageCellVoltage); Write_Text(phost, 170, 30, 20, txt);
  snprintf(txt, sizeof(txt), "Low: %.3fV", bms.LowCellVoltage); Write_Text(phost, 170, 40, 20, txt);
  snprintf(txt, sizeof(txt), "Pack: %.1fV", bms.PackVoltage); Write_Text(phost, 170, 50, 20, txt);

  insert_line(phost,300,500,0,80,20);
  Write_Text(phost,320, 0, 22, "Temperatures");
  snprintf(txt, sizeof(txt), "Mc: %d", (int)motor.HeatSinkTemp); Write_Text(phost, 330, 20, 20, txt);
  snprintf(txt, sizeof(txt), "Motor:%d", (int)motor.MotorTemp); Write_Text(phost, 330, 30, 20, txt);
  snprintf(txt, sizeof(txt), "CellHi: %d", bms.CellHighTemp); Write_Text(phost, 330, 40, 20, txt);
  snprintf(txt, sizeof(txt), "CellLo: %d", bms.CellLowTemp); Write_Text(phost, 330, 50, 20, txt);
  snprintf(txt, sizeof(txt), "Bms: %d", bms.InternalTemp); Write_Text(phost, 330, 60, 20, txt);
   
  snprintf(txt, sizeof(txt), "%dkm/h", (int)motor.VehicleVelocity); Write_Text(phost, 200, 200, 24, txt);

  if(state.SafeState) { safestate_icon(phost,100,140); }
  if(state.CCactive) { cruise_control_icon(phost,160,170,inputs.CCSpeed); }
  
  driving_mode_icon(phost,0,0,0,state.DriveButton);
  if(state.DriveButton) { ECO_mode_icon(phost,0,0,0,inputs.GasLimiter); }
  if(bms.BMSerror) { volt_battery_icon(phost,180,120,255,0,0); }
  if(motor.MCerror) { mc_icon(phost,250,120,255,255,0); }
  if(bms.HighTemp) { hightemp_battery_icon(phost, 110, 115, 255, 0, 0); }

  if(state.Hazard) {
    TurnL_icon(phost,40,200); TurnR_icon(phost,410,200);
  } else if(state.Left_Turn) { TurnL_icon(phost,40,200); } 
  else if(state.Right_Turn) { TurnR_icon(phost,410,200); } 

  Finish_Display(phost);
}