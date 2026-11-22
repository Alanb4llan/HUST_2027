#ifndef LED_FUNCTIONS_H
#define LED_FUNCTIONS_H

#include <Arduino.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define READ_SAFE_STATE 2
#define LEFT_BLINKER 15
#define RIGHT_BLINKER 16
#define BRAKE_LIGHT 7
#define READ_BRAKE_LIGHT 6
#define DAYTIME_RUNNING_LIGHTS 17
#define SAFE_STATE_LIGHT 21

extern int left_blinker;
extern int right_blinker;
extern int hazard_light;
extern int brake_light;
extern int drl;

void setupLEDs();
void blinkLEDs();

#endif