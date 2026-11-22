# Port plan: old ESP32 code → STM32L476RG (STM32duino)

Scope: the old main ESP32 (`old_code_esp32/Main_Ratt_Belgien26/Mainkod/`), the old steering-wheel ESP32 (`.../SteeringWheel/SteeringWheelCode20-09-26/`), the WIP sketch `firmware/HUST27/` and the test sketch `firmware/Display/`.
Pins refer to [pin_map.md](pin_map.md), which uses the schematic as the source of truth.
**GUESS** marks anything not backed by a file in this repo.

## 0. Board roles (decided)

**The STM32L476RG on the main board is the only MCU in the car.** It takes over everything the two old ESP32s did:
- old main board: CAN, lights, LoRa, SD
- old steering wheel: inputs, drive command 0x501, cruise control, driver display

The steering wheel has no MCU. Its buttons, pedals and the OLED display connect to the main board through harness connector J1:
- GAS (PB0, ADC), BRAKE (PB1), NEUTRAL (PC5), CC+OK_MODE (PA1), INDICATORS+HAZARDS (PA2)
- SCREEN_CS/DC/RST/BUSY on SPI1

Consequences:
- The old steering ↔ main CAN link (0x175/0x176) is **obsolete**. Lamp, brake and safe-state information is now read locally on the same MCU.
- The main board **transmits 0x501** (the drive command) itself.

## 1. Module by module

### 1.1 CAN, main board (`Mainkod/CAN_functions.*`) and steering wheel (`CanHandler.*`)
- **What it does.** Both decode motor controller (0x401–0x40E), BMS (0x601–0x605) and MPPT (0x200/0x210/0x220/0x230) frames into globals. Main sends 0x175 (brake switch, safe state) to the wheel. The wheel sends 0x501 (drive command) and 0x176 (indicators, hazard, brake). The main board also tracks Wh since start and zeroes MPPT power after 5 s without MPPT frames. See [can_ids.md](../can_protocol/can_ids.md).
- **STM32 changes**
  - `ESP32-TWAI-CAN` becomes **STM32_CAN (pazi88)** on CAN1, PB8 RX / PB9 TX, 500 kbit/s. `firmware/HUST27` already does this.
  - Use hardware filters (already set for 0x400/0x600/0x200 ranges). 0x175/0x176 are no longer needed (single MCU).
  - Replace pointer-cast float decoding (`*((float*)(buf+4))`) with `memcpy`, because unaligned VLDR can fault on Cortex-M4F and the cast is strict-aliasing undefined behaviour.
  - Keep `setAutoBusOffRecovery(true)` (see `docs/tips-and-tricks.txt`).
  - Read the RX queue every loop and send TX on a fixed 100 ms schedule.
- **Board.** Main.
- **Risks**
  - Old main code: `case 0x176` has no `break`, so it falls through into `0x501` and overwrites `driverRPM`/`driver_current` with indicator bytes.
  - Old main MPPT output-current sign test uses `data[2]` instead of `data[6]`.
  - BMS temperatures are decoded as `uint8_t`, so negative temperatures are impossible (**GUESS**: the Orion config may send signed values).
  - CAN bit timing depends on the clock source: there's no HSE, so use HSI16 or MSI+LSE trimming.

### 1.2 Drive command (steering `sendDriveCAN`, 0x501)
- **What it does.** Every 100 ms the wheel sends two floats: target motor RPM (20000 = forward torque mode, −100 = regen/brake, 0 = idle) and target current (0..1). Comments name a Tritium WaveSculptor.
- **STM32 changes.** Same frame via STM32_CAN, built with `memcpy`. Add:
  - an **IWDG watchdog** (`IWatchdog` library in STM32duino)
  - a rule that the command is zero current whenever inputs are invalid, the drive switch is off or safe state is active
  - a fixed transmit period driven by `millis()`, never blocked by SD or LoRa
- **Board.** Main.
- **Risks.** **GUESS:** the WaveSculptor stops the motor if commands stop arriving within a few hundred ms. Confirm with its manual. Reverse driving (reg 2.22.2) needs negative RPM with forward current. That isn't implemented in the old code (the only negative RPM is for braking).

### 1.3 Steering-wheel inputs (`Inputs.*`)
- **What it does**
  - Two pots (gas, brake) are read with `analogRead`, rejected if outside 500..3500 (12-bit), and auto-calibrated (min/max tracking) on the start screen.
  - Deadzones are +500 for gas and +400 for brake, then mapped to 0..`GasLimiter/5`.
  - Seven buttons on ESP32 interrupts (`IRAM_ATTR` ISRs set flags) with a 400 ms software debounce. They cover left/right turn, hazard, CC up/down, gear/OK (cycles GasLimiter 1..5 and leaves the start screen) and a drive-select switch.
- **STM32 changes**
  - On the main board the inputs are not 7 separate buttons. They are GAS PB0 (ADC12_IN15), BRAKE PB1 (ADC12_IN16), NEUTRAL PC5 (ADC12_IN14), **CC+OK_MODE PA1** and **INDICATORS+HAZARDS PA2**, each with a 10k pull-down.
  - Two functions per pin suggests resistor-ladder analog inputs (**unknown, ask**). Plan to read them with `analogRead` and threshold windows.
  - STM32duino `analogRead` defaults to 10-bit, so call `analogReadResolution(12)` before reusing the old 500/3500 limits.
  - Drop `IRAM_ATTR`. If any input is a plain digital button, use `attachInterrupt` or, simpler, poll every 5–10 ms with debounce (enough for buttons).
  - PB0 is only 3.6 V tolerant: confirm the pedal supply.
- **Board.** Main.
- **Risks**
  - The old code **disables the brake pedal**: `mapFloat(..., 0, 0)` with the comment "BRAKE TURNT OFF", so the brake is always 0. Regen braking and the brake-pedal cruise-control cancel never work.
  - Calibration exits on gas range > 300 only; the brake check is commented out.

### 1.4 Cruise control (`CruiseControl.cpp`)
- **What it does.** A PI controller (Kp 0.05, Ki 0.01, Kd unused) on speed error in km/h. It outputs a target current of 0..1 with a fixed RPM of 20000, runs every 100 ms, and does crude anti-windup (it undoes the last integral step on saturation). CC-down sets CC on at the current speed. CC up/down step in multiples of 5 km/h. Gas is ignored while CC is active.
- **STM32 changes.** Portable as is (pure math). Run it at a fixed rate from a `millis()` scheduler.
- **2027 addition: the 6-axis IMU is used by cruise control (team decision).** The main board's IC3 is a WSEN-ISDS 6-axis accelerometer + gyroscope, on SPI1 with CS PC3, INT0 PC6 and INT1 PA0. It will be implemented together with the car as part of cruise control. How the IMU data feeds the controller is **not decided yet**. **GUESS:** examples are incline/grade feed-forward from pitch, or acceleration feedback for smoother control. The IMU driver therefore becomes a dependency of cruise control.
- **Regulation 2.26.1.** Cruise control must cancel on brake or when the car is turned off, and must not resume automatically.
  - Cancel paths in the old code: the brake pedal (dead, see 1.3), 0x175 byte 0 from the main board brake switch (a CAN dependency), the drive switch off, and safe state.
  - On the main board, cancel **directly from the BRAKE input PB1** (and any brake-switch input) in the same loop.
- **Board.** Main.
- **Risks.** The integral can still wind up while error ≤ 0 (it is reset, which causes a jump). Fixed gains aren't tuned for the 2027 car. See section 4 (R1–R3) for what the port must do differently.

### 1.5 Lights (`Mainkod/LED_functions.*`)
- **What it does**
  - Blinkers toggle every 333 ms (90 flashes/min).
  - Hazard, and also safe state, blink both sides.
  - Brake/tail lamp uses PWM: 64/255 tail, 255 brake, driven by CAN 0x176 byte 3 **or** a hardware brake-light read pin.
  - DRL output is set HIGH at boot. A safe-state light blinks.
- **STM32 changes**
  - Pins: L_IND **PA9**, R_IND **PA8**, BRAKE_LIGHTS **PB3** (TIM2_CH2, so `analogWrite` PWM works), all low-side N-MOSFETs.
  - Drive the brake lamp from the local BRAKE input **PB1** (reg 2.23.15 must not depend on CAN).
  - The 333 ms toggle gives 90 flashes/min, inside 90±30 (reg 2.23.11). Keep blinking non-blocking.
  - PB3 is JTDO/SWO at reset. That's fine with SWD-only debugging, but don't enable SWO trace.
- **Board.** Main.
- **Risks / missing hardware.** There is **no DRL output, horn output or safe-state input** on the main board schematic. The DRL board is passive LEDs. This is an open question for the hardware team.

### 1.6 LoRa telemetry (`Mainkod/LoRa_functions.*`, `firmware/HUST27/LoRafunc.*`)
- **What it does**
  - The old code sends one ASCII, space-separated line of about 26 values every `sendInterval` (1 s), at 868 MHz, SF7, BW 125 kHz, sync word 0xF3.
  - The new code sends packed binary structs (types 0x01–0x04) or one consolidated 0xFF packet. That packet holds raw `float`/`double` (8 bytes for doubles), little-endian, plus a flags byte and a `uint16` counter.
- **STM32 changes**
  - The car radio is an **RFM95W-915S2 (SX1276)** on the LoRa TX board, behind the **LTC6820 isoSPI** link (CS PC0, RST PC7, DIO0 PA10, DIO1/"BUSY" PD2). So **sandeepmistry `LoRa.h` is the right library family.** Changes:
    - `LoRa.begin(915E6)`, not 868E6. The module is a 915 MHz part. Team Managers Guide p.36 (ACMA): pick an interference-free band. **GUESS:** the Australian LIPD class-licence band is 915–928 MHz.
    - `LoRa.setSPIFrequency(...)` well below the 8 MHz default. The LTC6820's maximum SPI clock is far lower, and SLOW is tied high on both boards. Get the limit from the LTC6820 datasheet, which isn't in the repo.
    - `LoRa.setPins(PC0, PC7, PA10)` and `LoRa.setSPI(SPI)` (SPI1 = PA5/PA6/PA7 on this variant: verify).
    - Use non-blocking send: `LoRa.endPacket(true)` (async) plus a DIO0 TX-done check, or at least no `delay()`.
    - Fail gracefully like the old code (`LoRaOK` flag with a 10 s timeout), not a `while(!begin)` loop.
  - **Pit receiver.** The `lora_rx` board is an **ESP32-S3 + SX1262**, so it needs RadioLib, not `LoRa.h`. **GUESS:** the SX127x sync word 0xF3 corresponds to SX126x 0xF434. RadioLib's `setSyncWord(0xF3)` handles the conversion. The receiver must parse the same packed binary layout (or use a versioned format with a CRC).
- **Board.** Main (radio on a remote board).
- **Risks.** Blocking airtime: SF7/125 kHz with about 50 bytes takes roughly 100 ms (**GUESS**). Old `sendLoRaData` busy-waits on `beginPacket()`. The isoSPI link adds latency, and the SPI bus is shared. Check that the LTC6820 `EN` pin tied to GND really enables the part.

### 1.7 SD logging (`Mainkod/SD_card.*`, `prepareAndWrite2SD`)
- **What it does.** Every 1 s it appends one space-separated text line of about 26 floats to `/log_N.txt`. N comes from an ESP32 NVS counter incremented at boot. The file is reopened for every append. Chip selects are toggled by hand around the shared SPI bus.
- **STM32 changes**
  - ESP32 `SD`/`FS` becomes **SdFat** (preferred) or the Arduino `SD` library on SPI1, CS **PC1**. The STM32SD/SDMMC library can't be used (SDMMC pins are taken).
  - Replace NVS: scan for the next free `log_N` name at boot (the old commented-out loop does this), or keep a counter file on the card. STM32duino `EEPROM` emulation also works but wears flash.
  - Keep the file open, write buffered, and `flush()`/`sync()` periodically (every few seconds) so a power cut loses little.
  - Add a header line and `millis()` timestamp. There's no absolute time: VBAT is tied to 3.3 V, so the RTC has no backup.
- **Board.** Main.
- **Risks.** SD writes can block for tens to hundreds of ms, so don't do them in the same time slice as the drive command or CAN. Challenger packs are disconnected and sealed from 19:15 to 06:15 (regs 3.28.8–3.28.9), so logging loses power overnight. Close and flush files cleanly.

### 1.8 Shared SPI1 bus (new concern, not in the old code)
SD (PC1), IMU WSEN-ISDS (PC3), LoRa isoSPI (PC0) and the screen on J1 (PC2) share SCK PA5, MISO PA6 and MOSI PA7.
- Drive **all four CS pins HIGH before any `begin()`**. An uninitialised SD card can corrupt the bus.
- Use `SPI.beginTransaction()` with per-device speed and mode. The LTC6820 is strapped for mode 0 and needs a slow clock.
- Never hold the bus across long SD operations while a LoRa or display transfer is due.

### 1.9 Driver display: old Riverdi EVE → new OLED
- **What the old code did.** A Riverdi EVE3 4.3" (FT81x/BT81x coprocessor) over SPI, using about 200 KB of vendor HAL (`Gpu_Hal*`, `CoPro_Cmds*`, `App_Common*`, `DispFunctions*`, `Hal_Utils*`, `Platform.h`, `Riverdi_Modules.h`). It had two screens:
  - a calibration start screen (gas/brake min/max)
  - the main screen: power, cell voltages, temperatures, speed, and icons for safe state, cruise control, drive/eco mode, BMS error, MC error, high temperature and indicators.
  It redrew at 10 Hz.
- **2027: an OLED display, exact model not chosen yet.** **Don't port the EVE HAL.** Keep only the screen content and layout ideas from `main_screen()`/`start_screen()`.
  - Connection: SPI1 via J1. SCREEN_CS = PC2, SCREEN_DC = PB4, SCREEN_RST = PC11. SCREEN_BUSY = PB5 is normally not used by OLEDs and can probably stay unused. Use a 4-wire SPI OLED, because the board has no I2C display wiring. If an I2C OLED is chosen, the only I2C-capable spare pins on J1 are PB6/PB7 (I2C1). **Don't** use the default `Wire` pins PB8/PB9, which are CAN.
  - Library: depends on the controller (e.g. SSD1306/SSD1309/SH1106/SSD1322). Candidates are Adafruit_SSD1306 (already used in `firmware/Display/`, and it supports hardware SPI) or U8g2. **Decide once the model is known, and ask before installing.**
  - The display is small, so prioritise: reg 2.25.1 requires **speed, indicator state, hazard state and ESS warnings (BMS error, high temperature) always visible**, not behind menus. Put everything else (cell voltages, temperatures, power) on secondary pages, or show it only when stopped. Reg 2.25.2 requires the display to be powered from the ESS (car 12 V), not a separate battery.
- **Board.** Main.
- **Risks.**
  - A full-frame SPI transfer for a 128×64 OLED is 1 KB, which is fast. For larger or greyscale OLEDs it is more. Never let a display refresh block CAN or the drive command, and use `SPI.beginTransaction()` because SPI1 is shared.
  - OLED burn-in from static content over long driving days. **GUESS:** consider a slight pixel shift.
  - Readability in direct sunlight. Pick a bright model.

### 1.10 `firmware/Display/` (SSD1306 OLED test sketch)
- **What it does.** A 128×64 I2C OLED at 0x3C. Three buttons toggle hazard/left/right, with a 500 ms blink (60 flashes/min, inside 90±30). Speed is simulated. It also initialises an unused DHT11 sensor.
- **STM32 changes.** A test only. Its pins (PA0–PA3) and default `Wire` pins (PB8/PB9 on Nucleo/generic L476 variants = **CAN**) conflict with the main board. **This is the most useful starting point for the 2027 OLED.** Reuse `drawScreen()`, the arrows and the speed centring, switch to the SPI constructor of Adafruit_SSD1306 on SCREEN_CS/DC/RST (if the chosen OLED is SSD1306-compatible), and take button/hazard state from the real inputs.
- **Board.** Main (after adapting).

### 1.11 Misc
- **Serial / debug.** Use **USB CDC** (PA11/PA12, J7). In the Arduino IDE set "USB support: CDC (generic Serial supersede U(S)ART)". Hardware USART1 and USART2 pins are used by board signals. Rate-limit prints.
- **Clock.** No HSE; LSE 32.768 kHz is present. Confirm the variant's `SystemClock_Config`, and prefer MSI with LSE PLL-mode for CAN accuracy.
- **IMU (WSEN-ISDS 6-axis accel+gyro on SPI1, CS PC3, INT0 PC6, INT1 PA0).** New, not in the old code. **It will be used by cruise control** (see 1.4). `datasheets/` has the ADXL312, which isn't on the board, so the WSEN-ISDS datasheet is needed before writing the driver.
- **Safe state.** The old main board read a safe-state pin, blinked hazards and forwarded it on 0x175. The 2027 main board has no such input. This is an open question for the hardware team. Reg 2.28 safe state must be hardware (not semiconductor-dependent), so firmware only *reports* it.

## 2. Suggested porting order

| # | Step | Why this order |
|---|---|---|
| 1 | Board bring-up: correct board/variant (generic L476RG), USB CDC Serial, clock check, one `board_pins.h` from pin_map.md, all SPI CS high, a blinking indicator | Everything else depends on correct pins |
| 2 | CAN RX decode and filters (fix casts, add MPPT4) with a serial printout | Already 80 % done. Needed by the display, LoRa and SD |
| 3 | Lights: indicators/hazard blink, brake lamp from local PB1, tail/brake PWM on PB3 | Regulation-critical (2.23.x) and simple |
| 4 | Inputs (ADC pedals, ladder buttons), then drive command 0x501 with watchdog and timeouts | Needed to drive. Safety-critical |
| 5 | IMU driver (WSEN-ISDS on SPI1), then cruise control with brake cancel from local inputs (2.26.1) and IMU input | Depends on 4. Cruise control uses the IMU |
| 6 | Driver OLED display (once the model is chosen), starting from `firmware/Display/` | Regulation 2.25. Depends on 2 and 4 |
| 7 | LoRa telemetry over isoSPI at 915 MHz with a low SPI clock, plus the matching pit receiver | Not needed to drive. Tricky hardware path |
| 8 | SD logging (SdFat, buffered) | Lowest risk to driving, last on the shared bus |


## 3. Problems in current `firmware/` (not fixed yet)

| # | File | Problem |
|---|---|---|
| 1 | `firmware/Display/Display.ino`, `Display.cpp` | `#include "display.h"`, but the file is `Display.h`. This breaks on case-sensitive file systems (Linux/macOS/CI) |
| 2 | `firmware/Display/Display.h` | Uses `Adafruit_SSD1306` without including its header. It only compiles because of include order |
| 3 | `firmware/Display/Display.ino` | Buttons on PA0/PA1/PA2 with `INPUT_PULLUP`, DHT on PA3: PA0 = IMU INT1, PA1/PA2 have 10k pull-downs, PA3 isn't connected. `Wire.begin()` defaults to PB8/PB9 = CAN. The DHT library is unused on this board. Speed is simulated and "TEST TEST" shows on hazard |
| 4 | `firmware/HUST27/HUST27.ino` | Includes STM32_CAN twice (`<STM32_CAN.h>` and `"STM32_CAN.h"`) |
| 5 | `HUST27.ino` | `pinMode(PA10, OUTPUT)` plus HIGH as "brake lights". PA10 is `LoRa_DIO0`, driven by the 74LVC125, so this causes **output contention**. The brake lights are on **PB3** |
| 6 | `HUST27.ino` | Indicators and brake lamp are held constantly HIGH: no blink logic, no brake input |
| 7 | `HUST27.ino` | `setupLoRa()` is never called, but `sendConsolidatedPacket()` runs every loop on an uninitialised radio |
| 8 | `firmware/HUST27/LoRafunc.cpp` | `LoRa.begin(868E6)`, but the module is an RFM95W-**915**. Also `while(!LoRa.begin)` retries forever, which hangs boot with no radio |
| 9 | `LoRafunc.cpp` | No `LoRa.setSPIFrequency()`. The library default (8 MHz) is far too fast for the LTC6820 isoSPI link |
| 10 | `LoRafunc.h` | Declares `sendLoRaTestMessage()` and `receiveLoRaMessage()`, which don't exist. Doesn't declare `handleLoRaTransmission()`, `sendLoRaHeartbeat()` or `sendCriticalData()` etc. The "Nucleo-L4R6G + RFM95W" pin comment is stale. No DIO1/BUSY (PD2) define |
| 11 | `LoRafunc.cpp` / `global.cpp` | `sendInterval` (and the unused `LORA_SCK/MISO/MOSI` defines) are dead. The const `LoRaSendInterval` is used instead. `sf`/`sbw` are only used in `setupLoRa()` |
| 12 | `LoRafunc.cpp` | `handleLoRaTransmission()` blocks with `delay(50)` ×4 plus airtime, starving CAN |
| 13 | `LoRafunc.cpp` | The consolidated packet sends raw `double` (8 bytes) and `float`, with no length, version or CRC. The receiver must match exactly. Only 2 flag bits are filled |
| 14 | `firmware/HUST27/global.h` | Comment says definitions live in HUST27.ino; they are in `global.cpp` |
| 15 | `firmware/HUST27/CANfunc.h/.cpp` | `sendDriveCAN()` and `sendDashboardCAN()` are declared but their bodies are commented out (a link error if called) |
| 16 | `CANfunc.cpp` | Obsolete with a single MCU: the commented-out `sendDashboardCAN()` (0x176) is no longer needed, because lamp state is local. `sendDriveCAN()` (0x501) must be **re-enabled**, because the main board now drives the motor controller. The current filters are fine for that |
| 17 | `CANfunc.cpp` | MPPT 4 (0x230) passes the filter but is ignored. `TotMPPT` only sums 3 |
| 18 | `CANfunc.cpp` | `*((float*)(rxMsg.buf + 4))` pointer-cast decoding: possible unaligned-access fault (VLDR) on Cortex-M4F and strict-aliasing undefined behaviour. Use `memcpy` |
| 19 | `CANfunc.cpp` | 0x401 error check only tests `buf[2]`. **GUESS** (Tritium spec): the error flags are 16-bit in bytes 2–3 |
| 20 | `CANfunc.cpp` | `Distance` (0x40E bytes 0–3) is printed as km. **GUESS:** the WaveSculptor odometer is in metres |
| 21 | `CANfunc.cpp` | `printTelemetryToSerial()` writes about 700 bytes every 100 ms. On a hardware USART at 115200 that is about 60 ms of blocking per call |
| 22 | All `Serial` use | Default `Serial` maps to a hardware USART (PA2/PA3 or PA9/PA10, depending on variant), and both collide with board signals. Use USB CDC |
| 23 | `CANfunc.cpp`, `LoRafunc.cpp/.h`, `global.h`, `Display.ino` | Mojibake (UTF-8 encoded twice) in comments, e.g. `SpÃ¤nning`, `Â°C`, `â€”`, `âš ï¸` |
| 24 | `hal_conf_extra.h` | Fine for L4. The F1/F3 blocks are inert boilerplate. Listed only so it isn't missed |

## 4. Old-code review: requirements for the STM32 port

A code review of `old_code_esp32/` (2026-11-22) found the problems below. The old code stays as it is, for reference only. Each row says what the new firmware must do instead.

| # | Old-code problem (file:line) | Requirement for the STM32 port |
|---|---|---|
| R1 | Brake pedal mapped to 0..0, so `inputs.Brake` is always 0 and the pedal never cancels cruise control. Cancelling relied on CAN 0x175, sent at most once per second (`Inputs.cpp:97`) | Cancel cruise control **in the same loop** the BRAKE input (PB1) shows braking. No CAN in that path. Never auto-resume (reg 2.26.1) |
| R2 | Cruise control uses `motor.VehicleVelocity` with no freshness check. If 0x403 stops, the integral grows until the current reaches 1.0 (`CruiseControl.cpp:19`) | Timestamp every decoded CAN value. If speed is older than a limit (e.g. 300 ms, to be tuned), **cancel cruise control and command zero current** |
| R3 | PI controller zeroes the current and resets the integral as soon as error ≤ 0, so speed oscillates. Gains apply per call, not per unit time (`CruiseControl.cpp:21`) | Proper PI with real `dt`, output clamping and anti-windup (conditional integration), with no reset at the setpoint. Use the IMU (WSEN-ISDS) as planned. Respect the eco/GasLimiter cap. Tune on the car |
| R4 | Old main loop reads one CAN frame per pass, gates all periodic work on "frame received", and blocks on LoRa (`while(beginPacket()==0) delay(100)`) and SD open/append/close, with a 5-frame RX queue (`Mainkod.ino:82`) | Drain the CAN RX queue with `while (Can.read(...))` every loop. Run each periodic task on its own `millis()` schedule, independent of RX. No `delay()` and no busy-waits in the main loop. Non-blocking LoRa (`endPacket(true)`). SD file kept open with buffered writes |
| R5 | Steering wheel reads the TWAI status and throws it away, so there's no bus-off recovery (`CanHandler.cpp:26`) | `Can.setAutoBusOffRecovery(true)` (already in HUST27.ino). Also count TX failures and show a CAN fault on the display |
| R6 | Hazard and an indicator can both be true. The CAN encoding (else-if) then drops hazard, so the lamps differ from the display (`CanHandler.cpp:119`, `Inputs.cpp:137/139`) | One lamp state machine with mutually exclusive modes `{OFF, LEFT, RIGHT, HAZARD}`, used for **both** the lamp outputs and the display |
| R7 | `case 0x176` falls through into `case 0x501` (`CAN_functions.cpp:171`) | Every `case` ends in `break`. Compile with `-Wimplicit-fallthrough` if possible |
| R8 | MPPT output-current sign taken from `data[2]` instead of `data[6]` (`CAN_functions.cpp:102`) | Decode 16-bit fields with one helper (`int16_t be16s(const uint8_t*)`) used everywhere |
| R9 | `mapFloat` can divide by zero (range exactly 500 gives NaN current). A range of 300–500 is accepted but leaves the pedal dead (`Inputs.cpp:90`) | Guard the divisor. Require a minimum calibrated range larger than the deadzone. Clamp the result to 0..limit and reject NaN before building 0x501 |
| R10 | `sprintf("CC:%d %", ...)`: lone `%` is undefined behaviour (`DispFunctions.cpp:434`) | Use `snprintf` with valid formats (`"CC:%d km/h"`) |

Also carried over from earlier analysis: replace `*((float*)(buf+4))` casts with `memcpy` (unaligned FPU loads fault on Cortex-M4F), and add a watchdog (IWDG) plus a zero-current default if the drive command can't be computed.
