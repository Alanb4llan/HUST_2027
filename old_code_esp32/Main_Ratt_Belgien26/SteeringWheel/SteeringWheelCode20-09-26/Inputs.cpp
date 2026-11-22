#include "Inputs.h"
#include "Globals.h"

// Define ISR flags
volatile bool flag_LeftTurn = false;
volatile bool flag_RightTurn = false;
volatile bool flag_Hazard = false;
volatile bool flag_CCUp = false;
volatile bool flag_CCDown = false;
volatile bool flag_Gear = false;
volatile bool flag_DriveSelect = false;

// ISR Functions (Lightweight flags)
void IRAM_ATTR isr_LeftTurn() { flag_LeftTurn = true; }
void IRAM_ATTR isr_RightTurn() { flag_RightTurn = true; }
void IRAM_ATTR isr_Hazard() { flag_Hazard = true; }
void IRAM_ATTR isr_CCUp() { flag_CCUp = true; }
void IRAM_ATTR isr_CCDown() { flag_CCDown = true; }
void IRAM_ATTR isr_Gear() { flag_Gear = true; }
void IRAM_ATTR isr_DriveSelect() { flag_DriveSelect = true; }

void PinSetup() {
  pinMode(GAS_POTENTIOMETER, INPUT); 
  pinMode(BRAKE_POTENTIOMETER, INPUT);  
  
  pinMode(LEFT_TURN_BUTTON, INPUT); 
  attachInterrupt(digitalPinToInterrupt(LEFT_TURN_BUTTON), isr_LeftTurn, RISING);
  
  pinMode(RIGHT_TURN_BUTTON, INPUT); 
  attachInterrupt(digitalPinToInterrupt(RIGHT_TURN_BUTTON), isr_RightTurn, RISING);
  
  pinMode(HAZARD_BUTTON, INPUT); 
  attachInterrupt(digitalPinToInterrupt(HAZARD_BUTTON), isr_Hazard, RISING);
  
  pinMode(CC_UP_BUTTON, INPUT); 
  attachInterrupt(digitalPinToInterrupt(CC_UP_BUTTON), isr_CCUp, RISING);
  
  pinMode(CC_DOWN_BUTTON, INPUT); 
  attachInterrupt(digitalPinToInterrupt(CC_DOWN_BUTTON), isr_CCDown, RISING);
  
  pinMode(OK_GEAR_BUTTON, INPUT); 
  attachInterrupt(digitalPinToInterrupt(OK_GEAR_BUTTON), isr_Gear, RISING);
  
  pinMode(DRIVE_SELECT_BUTTON, INPUT); 
  attachInterrupt(digitalPinToInterrupt(DRIVE_SELECT_BUTTON), isr_DriveSelect, CHANGE);
  state.DriveButton = digitalRead(DRIVE_SELECT_BUTTON);

  Serial.println("Arduino interrupt pinsetup done");
}

void CalibratePot() {
  inputs.Gas = analogRead(GAS_POTENTIOMETER);
  inputs.Brake = analogRead(BRAKE_POTENTIOMETER); 
  
  if (inputs.Gas < 500 || inputs.Gas > 3500 || inputs.Brake < 500 || inputs.Brake > 3500) {
    inputs.Gas = 0;
    inputs.Brake = 0;
  } else {
    if (inputs.Gas < inputs.MinGas) { inputs.MinGas = inputs.Gas; } 
    else if (inputs.Gas > inputs.MaxGas) { inputs.MaxGas = inputs.Gas; }

    if (inputs.Brake < inputs.MinBrake) { inputs.MinBrake = inputs.Brake; } 
    else if (inputs.Brake > inputs.MaxBrake) { inputs.MaxBrake = inputs.Brake; }
  }
}

void ReadPot() {
  inputs.Gas = analogRead(GAS_POTENTIOMETER);
  inputs.Brake = analogRead(BRAKE_POTENTIOMETER); 
  
  if (inputs.Gas < 500 || inputs.Gas > 3500 || inputs.Brake < 500 || inputs.Brake > 3500) {
    inputs.Gas = 0;
    inputs.Brake = 0;
  } else {
    // 1. Safely track the absolute lowest and highest physical positions
    if (inputs.Gas < inputs.MinGas) { inputs.MinGas = inputs.Gas; } 
    else if (inputs.Gas > inputs.MaxGas) { inputs.MaxGas = inputs.Gas; }

    if (inputs.Brake < inputs.MinBrake) { inputs.MinBrake = inputs.Brake; } 
    else if (inputs.Brake > inputs.MaxBrake) { inputs.MaxBrake = inputs.Brake; }
    
    // 2. Define fixed hardware deadzones (ignore first x units of travel)
    float activeMinGas = inputs.MinGas + 500;
    float activeMinBrake = inputs.MinBrake + 400;

    // 3. Map the Gas
    if (inputs.Gas < activeMinGas) {
      inputs.Gas = 0.0;
    } else {
      inputs.Gas = mapFloat(inputs.Gas, activeMinGas, inputs.MaxGas, 0, inputs.GasLimiter / 5.0);
    }

    // 4. Map the Brake
    if (inputs.Brake < activeMinBrake) {
      inputs.Brake = 0.0;
    } else {
      inputs.Brake = mapFloat(inputs.Brake, activeMinBrake, inputs.MaxBrake, 0, 0); //HEEEREEEE BRAKE TURNT OFFFFF change 0 to 1
    }
  }
  
  if (state.DriveButton && !state.SafeState) {
    if (inputs.Brake != 0) {
      state.CCactive = false;
      inputs.TargetCurrent = inputs.Brake;
      inputs.TargetRPM = -100;
    } else if (inputs.Gas != 0 && !state.CCactive) {
      inputs.TargetCurrent = inputs.Gas;
      inputs.TargetRPM = 20000;
    } else if (!state.CCactive) {
      inputs.TargetCurrent = 0;
      inputs.TargetRPM = 0;
    }
  } else {
    state.CCactive = false;
    inputs.TargetCurrent = 0;
    inputs.TargetRPM = 0;
  }
}

void ReadButtons() {
  static unsigned long lastDebounce = 0;
  bool handled = false;
  if (flag_DriveSelect) { 
    // Explicitly match the state to the physical pin (High = true, Low = false)
    state.DriveButton = digitalRead(DRIVE_SELECT_BUTTON); 
    handled = true; 
  }  
  // 400ms software debounce lock for physical buttons
  if (millis() - lastDebounce > 400) {


    if (flag_Gear) { 
      inputs.GasLimiter = (inputs.GasLimiter >= 5) ? 1 : inputs.GasLimiter + 1; 
      handled = true; 
    }
    
    if (flag_RightTurn) { state.Right_Turn = !state.Right_Turn; state.Left_Turn = false; handled = true; }
    if (flag_Hazard) { state.Hazard = !state.Hazard; state.Left_Turn = false; state.Right_Turn = false; handled = true; }
    if (flag_LeftTurn) { state.Left_Turn = !state.Left_Turn; state.Right_Turn = false; handled = true; }
    
    // Cruise Control Speed Selection Logic
    if (flag_CCUp) {
      if (state.CCactive) {
        inputs.CCSpeed++;
        while (inputs.CCSpeed % 5 != 0) { inputs.CCSpeed++; }
      }
      handled = true; 
    }
    
    if (flag_CCDown) {
      if (state.CCactive && inputs.CCSpeed > 0) {
        inputs.CCSpeed--;
        while (inputs.CCSpeed % 5 != 0) { inputs.CCSpeed--; }
      } else if (!state.CCactive) {
        inputs.CCSpeed = (int)motor.VehicleVelocity;
        state.CCactive = true;
        inputs.TargetCurrent = inputs.Gas; // Smooth transition from current pedal position
      }
      handled = true; 
    }
    
    // Allow start screen exit if potentiometers are somewhat calibrated
    if (inputs.MaxGas - inputs.MinGas > 300 &&  flag_Gear) { //ADD THIS CHECK WHEN BRAKE IS WORKING &&inputs.MaxBrake - inputs.MinBrake > 300 &&
      state.InStartScreen = false;
    }
    
    if (handled) {
      lastDebounce = millis();
    }
  }
  
  // Always clear the interrupt flags, even if ignored by debounce
  flag_LeftTurn = false; flag_RightTurn = false; flag_Hazard = false;
  flag_CCUp = false; flag_CCDown = false; flag_Gear = false; flag_DriveSelect = false;
}

float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}