#include "CruiseControl.h"
#include "Globals.h"

const float Kp = 0.05; 
const float Ki = 0.01; 
const float Kd = 0.00; 

float integralError = 0.0;
float lastError = 0.0;

void ProcessCruiseControl() {
  if (!state.CCactive) {
    integralError = 0.0;
    lastError = 0.0;
    return;
  }

  inputs.TargetRPM = 20000; 
  float error = (float)inputs.CCSpeed - motor.VehicleVelocity;
  
  if (error <= 0.0) {
    inputs.TargetCurrent = 0.0;
    integralError = 0.0; 
  } else {
    float P_out = Kp * error;
    integralError += error;
    float I_out = Ki * integralError;
    
    inputs.TargetCurrent = P_out + I_out;
    
    if (inputs.TargetCurrent > 1.0) {
      inputs.TargetCurrent = 1.0;
      integralError -= error; 
    } else if (inputs.TargetCurrent < 0.0) {
      inputs.TargetCurrent = 0.0;
      integralError -= error; 
    }
  }
  lastError = error;
}