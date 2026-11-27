# Main board pin map (STM32L476RGTx, LQFP-64)

**Sources**
- `hardware/main_pcb/*.kicad_sch`, read through a netlist exported with `kicad-cli sch export netlist` (KiCad 10). The schematic is treated as **authoritative**.
- `wiring/EXT_INT_PINOUTS.xlsx` (identical to `hardware/main_pcb/EXT_INT_PINOUTS.xlsx`).
- Alternate functions and ADC channels come from `datasheets/Main_PCB/MCU_DS_stm32l476rg.pdf` (DS10198 Rev 11, Table 16).

> ⚠️ **The spreadsheet and the schematic disagree.** The "NUCLEO MAPPING" sheet in the xlsx looks like an older Nucleo prototype. In it, PA9 is the right indicator, PA8 the left indicator, PA10 the brake lights, PB3 the screen reset, and LoRa uses PC10/PC11/PC12 on the Molex connector. The schematic (current PCB) has different assignments, and the "MOLEX 48" positions in the xlsx don't match the J1 pin names in the schematic either. **`HUST27.ino` follows the old spreadsheet.** See the conflicts section below. → **Question: is the schematic the current revision, and should the xlsx be updated?**

The package is confirmed in the schematic: `U1 = STM32L476RGTx`, footprint `LQFP-64_10x10mm_P0.5mm`. Note that `hardware/main_pcb/Reference STM32L476RG.png` is a generic EasyEDA reference design (it includes a BG96 modem and other parts that aren't on our board), so it is **not** a source for our pinout.

## Pin table

"0R" means a 0 Ω series link resistor (it can be removed to isolate the pin). "PD" means a pull-down to GND.
J1 = Molex 48-pin harness connector `5007620481`, J5 = RJ45 to the LoRa board, J7 = USB-C, J8 = microSD.

| Pin | MCU pin | Net | Function | Connects to | Notes |
|---|---|---|---|---|---|
| 1 | VBAT | +3.3V | Power | 3.3 V rail | No backup battery, so the RTC loses time at power-off |
| 2 | PC13 | PC13 | GPIO (spare) | 0R R10 → J1.J1 | |
| 3 | PC14 | OSC_IN | LSE | Y1 32.768 kHz | Don't use as GPIO |
| 4 | PC15 | OSC_OUT | LSE | Y1 32.768 kHz | Don't use as GPIO |
| 5 | PH0 | PH0 | GPIO (spare) | 0R R12 → J1.J3 | No HSE crystal fitted, so PH0/PH1 are free |
| 6 | PH1 | PH1 | GPIO (spare) | 0R R13 → **nothing** | Net label goes nowhere (xlsx says Molex F4) |
| 7 | NRST | — | Reset | S5 button + C7 | |
| 8 | PC0 | LoRa_CS | SPI1 CS | U2 LTC6820 `CS` → isoSPI → RFM95W NSS on LoRa TX board | |
| 9 | PC1 | SD_CS | SPI1 CS | J8 microSD DAT3/CD | SD card runs in SPI mode |
| 10 | PC2 | SCREEN_CS | SPI1 CS | J1.C4 | Driver OLED (model not chosen yet) |
| 11 | PC3 | SENS_ACC_CS | SPI1 CS | IC3 WSEN-ISDS IMU `CS` | |
| 14 | PA0 | SENS_ACC_INT1 | GPIO in / EXTI | IC3 `INT_1` | |
| 15 | PA1 | CC+OK_MODE | ADC12_IN6 / GPIO in | J1.K1 via 0R R30, 10k PD R31, TP10 | Two functions on one pin. Resistor ladder? **Unknown** |
| 16 | PA2 | INDICATORS+HAZARDS | ADC12_IN7 / GPIO in | J1.K3 via 0R R35, 10k PD R36, TP11 | Same question. PA2 is also USART2_TX |
| 17 | PA3 | PA3 | GPIO (spare) | 0R R27 → **nothing** | xlsx says Molex K1. PA3 is also USART2_RX |
| 20 | PA4 | PA4 | GPIO (spare) | 0R R3 → **nothing** | xlsx says Molex K2 |
| 21 | PA5 | SPI1_SCK | SPI1 | IC3 SCL, J8 CLK, U2 SCK, J1.D4 | Shared bus |
| 22 | PA6 | SPI1_MISO | SPI1 | 0R R28 → IC3 SAO, J8 DAT0, U2 MISO, J1.A4 | Shared bus |
| 23 | PA7 | SPI1_MOSI | SPI1 | IC3 SDA, J8 CMD, U2 MOSI, J1.K2 | Shared bus |
| 24 | PC4 | PC4 | GPIO (spare) | 0R R26 → **nothing** | xlsx says Molex J1 |
| 25 | PC5 | NEUTRAL | ADC12_IN14 / GPIO in | J1.J2 via 0R R43, 10k PD R44 | |
| 26 | PB0 | GAS | ADC12_IN15 | J1.H2 via 0R R39, 10k PD R40 | PB0 is **TT** (3.6 V tolerant, not 5 V) |
| 27 | PB1 | BRAKE | ADC12_IN16 / GPIO in | J1.G2 via 0R R41, 10k PD R42 | Analog pedal or switch? **Unknown** |
| 28 | PB2 | PB2 | GPIO (spare) | 0R R23 → J1.F2 | |
| 29 | PB10 | PB10 | GPIO (spare) | 0R R22 → J1.E2 | Also I2C2_SCL / USART3_TX |
| 30 | PB11 | PB11 | GPIO (spare) | 0R R21 → J1.A1 | Also I2C2_SDA / USART3_RX |
| 33 | PB12 | PB12 | GPIO (spare) | 0R R20 → J1.A3 | |
| 34 | PB13 | PB13 | GPIO (spare) | 0R R19 → J1.B1 | Also SPI2_SCK |
| 35 | PB14 | PB14 | GPIO (spare) | 0R R18 → J1.B3 | Also SPI2_MISO |
| 36 | PB15 | PB15 | GPIO (spare) | 0R R17 → J1.C1 | Also SPI2_MOSI |
| 37 | PC6 | SENS_ACC_INT0 | GPIO in / EXTI | IC3 `INT_0` | J1.C3 has a **separate** net labelled "PC6" that isn't connected to the MCU |
| 38 | PC7 | LoRa_RST | GPIO out | IC1 74LVC125 ch1 (1A→1Y) → J5.3 → LoRa board reset | |
| 39 | PC8 | PC8 | GPIO (spare) | 0R R15 → J1.D1 | |
| 40 | PC9 | PC9 | GPIO (spare) | 0R R14 → J1.D3 | |
| 41 | PA8 | R_IND | GPIO / TIM1_CH1 | R37 100R → Q3 DMN3023L gate (R38 10k PD) → J1.B2 `R_IND_OUT` (low side) | Lamp supply `R_IND_PS` J1.G4 via F3 2 A PPTC |
| 42 | PA9 | L_IND | GPIO / TIM1_CH2 | R29 → Q1 gate (R33 PD) → J1.C2 `L_IND_OUT` | Supply `L_IND_PS` J1.H4 via F2. PA9 is also USART1_TX |
| 43 | PA10 | LoRa_DIO0 | GPIO **in** / EXTI | IC1 ch2 (2A←J5.7, 2Y→PA10), TP12 | **Driven by the buffer, so never set it as OUTPUT.** Also USART1_RX |
| 44 | PA11 | USB- | USB FS | J7 USB-C (33R R48), D3 ESD | Good for Serial over USB CDC |
| 45 | PA12 | USB+ | USB FS | J7 USB-C (33R R49), D3 ESD | CC1/CC2 have 5.1k pull-downs (device role) |
| 46 | PA13 | PA13 | SWDIO | 0R R11 → J1.E1 | Keep it as SWD |
| 49 | PA14 | PA14 | SWCLK | 0R R5 → J1.E3 | Keep it as SWD |
| 50 | PA15 | PA15 | GPIO (spare) | 0R R6 → J1.F1 | JTDI by default |
| 51 | PC10 | PC10 | GPIO (spare) | 0R R7 → J1.F3 | |
| 52 | PC11 | SCREEN_RST | GPIO out | J1.A2 | |
| 53 | PC12 | PC12 | GPIO (spare) | 0R R8 → J1.G1 | |
| 54 | PD2 | LoRa_BUSY (via R9) | GPIO in | 0R R9 ← IC1 ch3 (3A←J5.8) | On the LoRa TX board this net is the **RFM95W DIO1** (named "BUSY") |
| 55 | PB3 | BRAKE_LIGHTS | GPIO / TIM2_CH2 (PWM) | R32 → Q2 gate (R34 PD) → J1.D2 `BRAKE_LIGHTS_OUT` | Supply `BRAKE_LIGHTS_PS` J1.F4 via F1. PB3 is JTDO/SWO at reset |
| 56 | PB4 | SCREEN_DC | GPIO out | J1.E4 | NJTRST at reset |
| 57 | PB5 | SCREEN_BUSY | GPIO in | 0R R2 ← J1.G3 | OLEDs normally have no BUSY line, so it can probably stay unused |
| 58 | PB6 | PB6 | GPIO (spare) | 0R R25 → J1.H1 | Also I2C1_SCL / USART1_TX |
| 59 | PB7 | PB7 | GPIO (spare) | 0R R4 → J1.H3 | Also I2C1_SDA / USART1_RX |
| 60 | BOOT0 | — | Boot | S4 to 3.3 V, R1 10k PD | |
| 61 | PB8 | CAN_RX | CAN1_RX (AF) | U4 SN65HVD232 `R` | Matches `STM32_CAN Can(PB8, PB9)` |
| 62 | PB9 | CAN_TX | CAN1_TX (AF) | U4 SN65HVD232 `D` | |
| 12/13 | VSSA/VDDA | GND/+3.3V | Power | | |
| 18,31,47,63 / 19,32,64 | VSS / VDD | | Power | | |
| 48 | VDDUSB | +3.3V | Power | | |

## Other board-level facts used by firmware

- **CAN**: SN65HVD232 (3.3 V, no standby pin). CAN_H/CAN_L go to J1.J4/K4, J2/J3 (WR-MPC3 6-pin: GND, GND, 12V, GND, CAN_L, CAN_H) and J4 (Micro-Fit 6-pin). S1 is a DP3T slide switch that selects split termination (R55/R57 60 Ω + C23 4.7 nF, or R56/R58 30 Ω + C24).
- **LoRa**: the radio is **not on the main board**. SPI1 → U2 LTC6820 (isoSPI master: MSTR=3.3 V, SLOW=3.3 V, POL=PHA=GND, so SPI mode 0) → T1 → J5 pins 4/5 → LoRa TX board (second LTC6820 as slave → **RFM95W-915S2**, an SX1276 module at 915 MHz). RST, DIO0 and DIO1/"BUSY" are buffered by 74LVC125s on both boards. J5: 1=+12V, 2=GND, 3=RST, 4/5=isoSPI, 6=GND, 7=DIO0, 8=BUSY(DIO1).
  - ⚠️ On **both** LTC6820s, pin `EN` is tied to GND. Check the LTC6820 datasheet (it isn't in `datasheets/`) to confirm the part runs with EN low. If EN is active-high, isoSPI is disabled.
- **IMU**: IC3 is a **Würth WSEN-ISDS 2536030320001** (6-axis accel+gyro, SPI/I2C), wired for SPI. `datasheets/` contains the **ADXL312**, which is **not** on the schematic. → **Question: is the ADXL312 planned, or should we get the WSEN-ISDS datasheet?**
- **SD**: microSD J8 in SPI mode (DAT1, DAT2 and card-detect unconnected). The SDMMC pins (PC8–PC12, PD2) are used for other things, so the STM32 SDMMC peripheral can't be used.
- **Power**: VIN is a diode-OR of USB 5 V (D1) and +12 V (D2 via F4). U5 is a Würth MagI³C buck to 3.3 V, and its PG output isn't routed to the MCU. Lamp outputs switch the low side through N-MOSFETs. Their supplies come back in from the harness through 2 A PPTC fuses.
- **Clock**: there's no HSE crystal, only LSE 32.768 kHz. For CAN bit timing, use HSI16 or MSI with LSE PLL-mode trimming (MSIPLLEN). Check which clock config the STM32duino variant you pick actually uses.
- **UART**: no dedicated debug UART is routed. Both USART1 (PA9/PA10) and USART2 (PA2/PA3) collide with board signals, so **use USB CDC (PA11/PA12) for `Serial`**.

## Conflicts with current code

| Code | What the code does | What the schematic says | Severity |
|---|---|---|---|
| `firmware/HUST27/HUST27.ino` | `pinMode(PA10, OUTPUT)`, drives HIGH as "Brake lights" | PA10 = `LoRa_DIO0`, an **output of the 74LVC125**. Driving it causes output contention. Brake lights are on **PB3** | **High** |
| `HUST27.ino` | PA8 = right indicator, PA9 = left indicator | Matches the schematic (R_IND=PA8, L_IND=PA9). The xlsx has them swapped | OK (xlsx wrong) |
| `firmware/HUST27/LoRafunc.h` | `LORA_DIO0 PA10` | Matches the schematic, but conflicts with the brake-light use above | (see above) |
| `LoRafunc.h` | `LORA_SS PC0`, `LORA_RST PC7` | Matches the schematic | OK |
| `LoRafunc.h` | Comment says "Nucleo-L4R6G + RFM95W, D10/D9/D2" | Board is an STM32L476RG. The radio sits behind isoSPI on another board | Stale comment |
| `LoRafunc.h` | No BUSY/DIO1 pin defined | PD2 carries RFM95W DIO1 | Missing (only needed for some modes) |
| `firmware/HUST27/global.cpp` | `STM32_CAN Can(PB8, PB9)` (RX, TX) | PB8=CAN_RX, PB9=CAN_TX | OK |
| `firmware/Display/Display.ino` | Buttons on PA0/PA1/PA2, DHT11 on PA3 | PA0 = IMU INT1 (driven by IC3). PA1/PA2 are harness inputs with 10k pull-downs (`INPUT_PULLUP` fights them). PA3 isn't connected | High if flashed on this board |
| `Display.ino` | `Wire.begin()` default pins, SSD1306 at 0x3C | On Nucleo/generic L476 variants the default I2C1 pins are usually **PB8/PB9 = CAN**. The OLED must go on SPI1 (SCREEN_CS PC2, DC PB4, RST PC11). If an I2C OLED is chosen anyway, use PB6/PB7 | High if merged |
| `HUST27.ino`, `Display.ino` | `Serial.begin()` | Default `Serial` is a hardware USART on PA2/PA3 or PA9/PA10, depending on variant. Both collide with board signals | Medium. Use USB CDC |
| Old ESP32 code | Brake-light PWM, DRL output, safe-state input, horn | The main board has **no DRL, horn or safe-state net**. The DRL board is passive (3×3 white LEDs, 2-wire input) | Open question (being asked to the hardware team) |

## Open questions

The STM32L476RG is the only MCU in the car (answered). The driver display is an OLED, model not chosen yet (answered).

| # | Question | Status |
|---|---|---|
| 1 | Which is current for J1 pin positions: the schematic or the xlsx "MOLEX 48" table? | Deferred. Firmware uses the schematic |
| 2 | Are CC+OK_MODE (PA1) and INDICATORS+HAZARDS (PA2) resistor-ladder analog inputs, and are GAS/BRAKE analog pots (PB0 is only 3.6 V tolerant)? | Deferred, needed before the input code is written |
| 3 | Where are the horn, DRL switching and safe-state sense handled? | Being asked to the hardware team |
| 4 | Dangling 0 Ω pins (PA3, PA4, PC4, PH1), the "PC6" net on J1.C3, LTC6820 `EN` tied to GND | Deferred. Hardware team's concern; only matters if LoRa doesn't work |
