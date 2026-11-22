# HUST27 – solar car firmware (BWSC 2027)

Firmware for HUST's Bridgestone World Solar Challenge 2027 car. The old ESP32 firmware is being rewritten for a new STM32 main board.

## Fixed decisions (don't propose alternatives)
- MCU: **STM32L476RGTx, LQFP-64** (confirmed in `hardware/main_pcb/MCU.kicad_sch`, U1)
- Framework: **Arduino core for STM32 (STM32duino)**
- CAN: **STM32_CAN (pazi88)**, CAN1 on **PB8 = RX, PB9 = TX**, 500 kbps, 11-bit standard IDs

## Repo layout
- `firmware/HUST27/`: new STM32 sketch (main target, work in progress)
- `firmware/Display/`: separate SSD1306 OLED/button test sketch (its own setup/loop, not wired to this board)
- `old_code_esp32/Main_Ratt_Belgien26/Mainkod/`: old main ESP32 (CAN, LoRa, SD, lights)
- `old_code_esp32/Main_Ratt_Belgien26/SteeringWheel/`: old steering-wheel ESP32 (inputs, cruise control, drive command, Riverdi EVE display)
- `hardware/main_pcb/`: main board KiCad project (sheets MCU, Power, Peripheral, InputsOutputs). `hardware/lora_tx/`, `lora_rx/`, `drl/` are the other boards. `hardware/_source_zips/` is gitignored
- `wiring/EXT_INT_PINOUTS.xlsx`: connector pinouts (**outdated vs. schematic**, see `docs/pin_map.md`)
- `datasheets/`: STM32L476, ADXL312 (the ADXL312 is **not** on the schematic; the board uses a Würth WSEN-ISDS IMU)
- `regulations/`: 2027 BWSC regulations. **Event Regulations V1.0** is the one that matters
- `can_protocol/can_ids.md`: CAN ID map
- `docs/`: `pin_map.md`, `port_plan.md`, `regulations_electrical.md`, `tips-and-tricks.txt`
- `graphify-out/`: knowledge graph (`graph.json`, `GRAPH_REPORT.md`, `graph.html`) plus `converted/` text versions of the netlists, xlsx and PDFs. Query it with `graphify query "..."`. It is **gitignored and local only**; if it's missing, rebuild it with `/graphify`

KiCad files are plain text. For pin/net questions, export a netlist (`"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" sch export netlist hardware/main_pcb/HUVUD_PCB.kicad_sch -o out.net`) or read `graphify-out/converted/main_pcb_netlist.md`.

## Board roles
- **Main board** (STM32L476RG): **the only MCU in the whole car.** It covers the CAN node, the drive command to the motor controller (0x501), cruise control, lamp drivers (indicators, brake), harness inputs (gas, brake, neutral, CC/OK, indicator/hazard), the driver OLED display on SPI1, microSD logging, the IMU, LoRa telemetry over isoSPI, and USB-C.
- **LoRa TX board** (`lora_tx`, in the car): RFM95W-**915**S2 (SX1276) behind an LTC6820 isoSPI slave. No MCU. Connected to the main board by RJ45 (J5).
- **LoRa RX board** (`lora_rx`, pit/chase): ESP32-S3 + SX1262 + microSD + USB.
- **DRL board** (`drl`): passive, 3×3 white LEDs. No MCU.
- **Steering wheel**: **no MCU**. The buttons, pedals and OLED are wired to the main board through J1. (The old car had a separate steering-wheel ESP32. Its logic moves into the main board.)
- **IMU**: the main board's 6-axis accelerometer + gyroscope (Würth WSEN-ISDS, SPI1, CS PC3, INT0 PC6, INT1 PA0) **will be used by cruise control**. How it feeds the controller is not decided yet.
- **Driver display**: **OLED**, exact model not chosen yet. It sits on SPI1 (SCREEN_CS PC2, DC PB4, RST PC11; BUSY PB5 is probably unused for an OLED). Ask before adding a display library.

## Key main-board pins (full list in `docs/pin_map.md`)
| Function | Pin | Function | Pin |
|---|---|---|---|
| CAN RX / TX | PB8 / PB9 | SPI1 SCK/MISO/MOSI | PA5 / PA6 / PA7 |
| Left / right indicator | PA9 / PA8 | Brake lights | **PB3** (not PA10) |
| GAS / BRAKE (ADC) | PB0 / PB1 | NEUTRAL | PC5 |
| CC+OK_MODE / IND+HAZARDS | PA1 / PA2 | LoRa CS / RST | PC0 / PC7 |
| LoRa DIO0 (input!) | PA10 | LoRa DIO1 ("BUSY") | PD2 |
| SD CS | PC1 | IMU CS / INT0 / INT1 | PC3 / PC6 / PA0 |
| Screen CS/DC/RST/BUSY | PC2 / PB4 / PC11 / PB5 | USB D- / D+ | PA11 / PA12 |
| SWDIO / SWCLK | PA13 / PA14 | | |

No HSE crystal, only LSE 32.768 kHz. VBAT is tied to 3.3 V, so there's no RTC backup. Use **USB CDC for `Serial`**, because the hardware USART pins are taken.

## CAN IDs (details in `can_protocol/can_ids.md`)
- Motor controller (Tritium WaveSculptor, assumed): status 0x401, bus V/I 0x402, RPM + velocity m/s 0x403, temps 0x40B, odometer/Ah 0x40E. Floats, little-endian. Filter 0x400/0x7F0.
- Drive command **0x501**: float RPM setpoint + float current 0..1, every 100 ms.
- BMS (Orion-style custom frames): temps 0x601, pack I/V and min/max cell 0x602, avg cell 0x603, error flags 0x605. Big-endian integers. Filter 0x600/0x7F8.
- MPPTs 0x200 / 0x210 / 0x220 / 0x230: Vin/Iin/Vout/Iout, big-endian. Filter 0x200/0x7C0.
- Old steering ↔ main: **0x176** (steering → main: left, right, hazard, brake) and **0x175** (main → steering: brake light, safe state). These are **obsolete in 2027** because there is only one MCU. The main board now sends 0x501 itself.
- **0x177**: MPPT IV-sweep command (per team, not in code; payload unknown).

## Key rules (details in `docs/regulations_electrical.md`)
- Indicators flash at 90±30 per minute (2.23.11). Hazard = both sides (2.23.12).
- Stop lamps on whenever driving is possible and brakes are applied (2.23.15). DRLs on whenever driving is possible (2.23.16).
- Horn per UNECE R28 (2.24.1).
- Always visible to the driver: speed, indicator status, hazard status, energy storage warnings (2.25.1). Must be powered from the car's energy storage (2.25.2).
- Cruise control cancels on brake or power-off and must never auto-resume (2.26.1).
- BMS must automatically keep cells within their V/I/T limits (2.5.6). Safe state must be fail-safe and must not depend on semiconductors (2.28.x). Isolation monitoring device required (2.27.9).
- Organiser tracker needs an RF-clear 120° cone (2.9.2). Voice radio must work in safe state (3.8.1).

## Working rules
- The embedded (firmware) team controls this project. The hardware is the hardware team's business: only flag hardware issues that are **dangerous** or that **block the firmware**, and don't do general hardware reviews.
- Don't invent hardware details. If it isn't in the schematics or datasheets, say "unknown" and ask.- Prefer small, targeted changes over rewrites.
- Work on the current branch. Commit only when asked, and never push.
- Ask before installing libraries or changing the folder structure.
- Never add Claude/AI attribution to commits, PRs, code or docs.

## Known open issues (see `docs/port_plan.md` for the full list)
- `HUST27.ino` drives PA10 (LoRa DIO0, a buffer output) as the brake-light output. Brake lights are PB3.
- LoRa code uses 868 MHz, but the module is 915 MHz. `setupLoRa()` is never called. The default 8 MHz SPI clock is too fast for isoSPI.
- `Display.ino` includes `"display.h"` but the file is `Display.h`. `HUST27.ino` includes `STM32_CAN.h` twice.
