#include "LED_functions.h"

// Variables for blinking LEDs
int count = 0;
unsigned long previousMillisLEDs = 0;
const int blinkInterval = 333;
bool ledState = LOW;
bool brakeLedState = LOW;
int tailLightPWM = 64;   // ~25% duty cycle for running lights (tune this for visual contrast)
int brakeLightPWM = 255; // 100% duty cycle for braking

int left_blinker;
int right_blinker;
int hazard_light;
int brake_light;
int horn;
int drl;
extern bool safeState;

void setupLEDs(){

  // Blinkers setup
  pinMode(LEFT_BLINKER, OUTPUT);
  digitalWrite(LEFT_BLINKER, LOW);

  pinMode(RIGHT_BLINKER, OUTPUT);
  digitalWrite(RIGHT_BLINKER, LOW);

  pinMode(BRAKE_LIGHT, OUTPUT);
  digitalWrite(BRAKE_LIGHT, LOW);
  pinMode(READ_BRAKE_LIGHT, INPUT);

  pinMode(DAYTIME_RUNNING_LIGHTS, OUTPUT);
  digitalWrite(DAYTIME_RUNNING_LIGHTS, HIGH);

  pinMode(SAFE_STATE_LIGHT, OUTPUT);
  digitalWrite(SAFE_STATE_LIGHT, LOW);

  pinMode(READ_SAFE_STATE, INPUT);
}

void blinkLEDs() {

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillisLEDs >= blinkInterval) {
    previousMillisLEDs = currentMillis;
    ledState = !ledState;

    // Blink LEDS
    if (left_blinker || hazard_light || safeState) {
      digitalWrite(LEFT_BLINKER, ledState);
      //Serial.println("LEFT BLINKER or hazard");
    } else {
      digitalWrite(LEFT_BLINKER, LOW);
    }

    if (right_blinker|| hazard_light || safeState) {
      digitalWrite(RIGHT_BLINKER, ledState);
      //Serial.println("RIGHT BLINKER or hazard");
    } else {
      digitalWrite(RIGHT_BLINKER, LOW);
    }
    if (safeState) {
      digitalWrite(SAFE_STATE_LIGHT, ledState);
      //Serial.println("RIGHT BLINKER or hazard");
    } else {
      digitalWrite(SAFE_STATE_LIGHT, LOW);
    }
  }
  if (brake_light || digitalRead(READ_BRAKE_LIGHT)) {
    analogWrite(BRAKE_LIGHT, brakeLightPWM);
    
    // Serial.println("BRAKE LIGHT"); 
  } else {
    analogWrite(BRAKE_LIGHT, tailLightPWM);
  }
}