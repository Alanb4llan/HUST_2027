#pragma once

// UI functions
void drawScreen();
void drawLeft(bool on);
void drawRight(bool on);
int getSpeedX(int value);

// ================= GLOBAL STATE =================
// (kept external for multi-file STM32 build)

// WARNING: ensure ONLY ONE definition exists in .ino

extern bool hazard;
extern bool leftActive;
extern bool rightActive;
extern bool blinkState;
extern int speed;

extern Adafruit_SSD1306 display;