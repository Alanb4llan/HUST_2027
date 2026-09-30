#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

#include "display.h"

// ================= SCREEN =================
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ================= BUTTONS (CHANGE FOR YOUR BOARD) =================
// ⚠️ These are placeholders — uncomment and set correct pins for your STM32
#define BTN_HAZARD PA0
#define BTN_RIGHT  PA1
#define BTN_LEFT   PA2

// ================= DHT (OPTIONAL HARDWARE) =================
#define DHTPIN PA3
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// ================= STATES =================
bool hazard = false;
bool leftActive = false;
bool rightActive = false;

bool lastHazardState = HIGH;
bool lastLeftState = HIGH;
bool lastRightState = HIGH;

bool blinkState = false;

// ================= SPEED =================
int speed = 1;

// ================= TIMERS =================
unsigned long lastBlink = 0;
unsigned long lastSpeedUpdate = 0;

// ================= SETUP =================
void setup() {

  Serial.begin(115200);

  // STM32 Wire init (default I2C pins depend on board)
  Wire.begin();

  // Buttons
  pinMode(BTN_HAZARD, INPUT_PULLUP);
  pinMode(BTN_RIGHT, INPUT_PULLUP);
  pinMode(BTN_LEFT, INPUT_PULLUP);

  // DHT (OK even if not used yet)
  dht.begin();

  // OLED init
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    while (true); // stop if display fails
  }

  display.clearDisplay();
  display.display();
}

// ================= LOOP =================
void loop() {

  bool hazardBtn = digitalRead(BTN_HAZARD);
  bool rightBtn = digitalRead(BTN_RIGHT);
  bool leftBtn = digitalRead(BTN_LEFT);

  if (hazardBtn == LOW && lastHazardState == HIGH) {
    hazard = !hazard;

    if (hazard) {
      leftActive = false;
      rightActive = false;
    }
  }
  lastHazardState = hazardBtn;

  if (leftBtn == LOW && lastLeftState == HIGH) {
    leftActive = !leftActive;

    if (leftActive) {
      rightActive = false;
      hazard = false;
    }
  }
  lastLeftState = leftBtn;

  if (rightBtn == LOW && lastRightState == HIGH) {
    rightActive = !rightActive;

    if (rightActive) {
      leftActive = false;
      hazard = false;
    }
  }
  lastRightState = rightBtn;

  // ================= BLINK =================
  if (millis() - lastBlink >= 500) {
    blinkState = !blinkState;
    lastBlink = millis();
  }

  // ================= SPEED SIMULATION =================
  if (millis() - lastSpeedUpdate >= 80) {
    lastSpeedUpdate = millis();

    speed++;
    if (speed > 150) speed = 1;
  }

  drawScreen();
}