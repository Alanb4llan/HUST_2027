#include <Arduino.h>
#include <Adafruit_SSD1306.h>
#include "display.h"

// ================= EXTERNAL VARIABLES =================
extern Adafruit_SSD1306 display;

extern bool hazard;
extern bool leftActive;
extern bool rightActive;
extern bool blinkState;
extern int speed;

// ================= ARROWS =================
void drawLeft(bool on) {
  if (on) {
    display.fillTriangle(0, 40, 19, 24, 19, 56, WHITE);
  }
}

void drawRight(bool on) {
  if (on) {
    display.fillTriangle(127, 40, 108, 24, 108, 56, WHITE);
  }
}

// ================= SPEED CENTERING =================
int getSpeedX(int value) {
  int digits = (value >= 100) ? 3 : (value >= 10) ? 2 : 1;
  int textWidth = digits * 32;
  return 69 - (textWidth / 2);
}

// ================= MAIN DISPLAY =================
void drawScreen() {

  display.clearDisplay();
  display.setTextColor(WHITE);

  if (hazard) {
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.print("TEST TEST");
  }

  if (hazard && blinkState) {
    drawLeft(true);
    drawRight(true);
  } 
  else {
    if (leftActive && blinkState) drawLeft(true);
    if (rightActive && blinkState) drawRight(true);
  }

  display.setTextSize(5);
  display.setCursor(getSpeedX(speed), 28);
  display.print(speed);

  display.display();
}