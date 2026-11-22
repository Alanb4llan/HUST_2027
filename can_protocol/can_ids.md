# HUST CAN bus: identifier map

**Bus**: 500 kbit/s, CAN 2.0A, 11-bit standard IDs, DLC 8 on every frame seen in code.

**Sources**: every ID below was found in one of these files:
- Old main ESP32: `old_code_esp32/Main_Ratt_Belgien26/Mainkod/Mainkod/CAN_functions.cpp`
- Old steering wheel ESP32: `old_code_esp32/Main_Ratt_Belgien26/SteeringWheel/SteeringWheelCode20-09-26/Globals.h`, `CanHandler.cpp`, `Inputs.cpp`, `CruiseControl.cpp`
- New STM32: `firmware/HUST27/CANfunc.cpp`, `firmware/HUST27/HUST27.ino` (filters)

**Conventions**
- `float` = IEEE-754 single, **little-endian**. It is copied raw into or out of the frame; both ESP32 and STM32 are little-endian.
- Integer fields are **big-endian** (MSB first) unless stated otherwise.
- Byte 0 = first data byte.
- **GUESS** = inferred, or taken from external spec knowledge rather than the repo. Verify before relying on it.
- **unknown** = no information in the repo.

## 2027 car: STM32 main board (one MCU for the whole car)

Source: `firmware/HUST27/`. The 2027 code reuses the 2025 IDs, so it **assumes the same motor controller, BMS and MPPTs as 2025**. Confirm that.

| ID | Dec | Name | Direction | Period | Status in current `firmware/HUST27` |
|---|---|---|---|---|---|
| 0x501 | 1281 | Motor drive command | **Main board → MC** | 100 ms (planned) | `sendDriveCAN()` declared, body commented out. Must be re-enabled |
| 0x401 | 1025 | MC status | MC → main board | unknown | Decoded (`MCerror`) |
| 0x402 | 1026 | MC bus measurement | MC → main board | unknown | Decoded (current only) |
| 0x403 | 1027 | MC velocity | MC → main board | unknown | Decoded (km/h) |
| 0x40B | 1035 | MC temperatures | MC → main board | unknown | Decoded |
| 0x40E | 1038 | MC odometer & bus Ah | MC → main board | unknown | Decoded (distance only) |
| 0x601 | 1537 | BMS temperatures | BMS → main board | unknown | Decoded |
| 0x602 | 1538 | BMS pack data | BMS → main board | unknown | Decoded |
| 0x603 | 1539 | BMS average cell voltage | BMS → main board | unknown | Decoded |
| 0x605 | 1541 | BMS error flags | BMS → main board | unknown | Decoded (`BMSerror`) |
| 0x200 | 512 | MPPT 1 data | MPPT 1 → main board | unknown | Decoded (output power) |
| 0x210 | 528 | MPPT 2 data | MPPT 2 → main board | unknown | Decoded (output power) |
| 0x220 | 544 | MPPT 3 data | MPPT 3 → main board | unknown | Decoded (output power) |
| 0x230 | 560 | MPPT 4 data | MPPT 4 → main board | unknown | Passes the filter but **not decoded** |
| 0x177 | 375 | MPPT IV-sweep command | unknown | unknown | **Not in code.** Payload unknown |

Not used in 2027: 0x175 and 0x176. Those were the link between the two 2025 ESP32s, and lamps, brake and safe state are now read locally. See also the [filters](#filters-in-hust27ino-2027) section.

## 2025 car: old ESP32 main board + ESP32 steering wheel

Sources: `old_code_esp32/Main_Ratt_Belgien26/Mainkod/` ("old main") and `.../SteeringWheel/SteeringWheelCode20-09-26/` ("steering").

| ID | Dec | Name | Sender → Receiver(s) | Period | Encoded / decoded in |
|---|---|---|---|---|---|
| 0x175 | 373 | Main status to steering wheel | Old main → steering | ~1 s (see notes) | Old main TX (`sendCAN2steeringWheel`), steering RX (`CanReadAll`) |
| 0x176 | 374 | Lights / brake request | Steering → old main | 100 ms | Steering TX (`sendESPCAN`), old main RX |
| 0x501 | 1281 | Motor drive command | **Steering → MC** (old main also listens) | 100 ms | Steering TX (`sendDriveCAN`), old main RX (logging) |
| 0x401 | 1025 | MC status | MC → steering | unknown | Steering only (old main ignores it) |
| 0x402 | 1026 | MC bus measurement | MC → old main, steering | unknown | Both |
| 0x403 | 1027 | MC velocity | MC → old main, steering | unknown | Both (the old main keeps m/s, steering converts to km/h) |
| 0x40B | 1035 | MC temperatures | MC → old main, steering | unknown | Both |
| 0x40E | 1038 | MC odometer & bus Ah | MC → old main, steering | unknown | Both |
| 0x601 | 1537 | BMS temperatures | BMS → old main, steering | unknown | Both |
| 0x602 | 1538 | BMS pack data | BMS → old main, steering | unknown | Both |
| 0x603 | 1539 | BMS average cell voltage | BMS → old main, steering | unknown | Both |
| 0x605 | 1541 | BMS error flags | BMS → steering | unknown | Steering only (old main ignores it) |
| 0x200 | 512 | MPPT 1 data | MPPT 1 → old main, steering | unknown | Both |
| 0x210 | 528 | MPPT 2 data | MPPT 2 → old main, steering | unknown | Both |
| 0x220 | 544 | MPPT 3 data | MPPT 3 → old main, steering | unknown | Both |
| 0x230 | 560 | MPPT 4 data | MPPT 4 → old main, steering | unknown | Both |
| 0x177 | 375 | MPPT IV-sweep command | unknown → MPPTs | unknown | **Not in the code.** Reported by the team as used on the old car |

## Devices (both cars)

The motor controller is a **Tritium WaveSculptor** according to the comment in `CANfunc.cpp` ("TRITON/WAVESCULPT"). The 0x400 base address and the 0x500 driver-control base match WaveSculptor defaults. **GUESS**: the model is not confirmed anywhere in the repo.
The BMS is "Orion BMS style" (comment in `CANfunc.cpp`). Orion messages are user-configured, so the layouts below describe **what our code decodes**, not a fixed spec.
The MPPTs are "DILITHIUM/CUSTOM" (comment in `CANfunc.cpp`). The model is unknown.

The byte layouts below are shared by both cars, because the devices (and their IDs) are the same. Notes say where the 2025 and 2027 code decode things differently.

---

## 2025 only: steering wheel ↔ main board (team-defined, not used in 2027)

> These two messages linked the two ESP32s in the 2025 car. In 2027 there is **one MCU** and the steering wheel has no MCU, so they're documented only for reading the old code.

### 0x175: main board status → steering wheel
Encoded in old main `sendCAN2steeringWheel(digitalRead(READ_BRAKE_LIGHT), safeState)`. Decoded in steering `CanReadAll` (`CAN_ID_ESP_RX`).

| Byte | Content | Type | Values |
|---|---|---|---|
| 0 | Brake light active (hardware brake switch, ESP32 GPIO 6 `READ_BRAKE_LIGHT`) | uint8 | 0 / 1 |
| 1 | Safe state active (`!digitalRead(READ_SAFE_STATE)`, GPIO 2) | uint8 | 0 / 1 |
| 2–7 | Padding | uint8 | 0xAA (stated purpose: to avoid bit-stuffing) |

- **Period**: sent when `sendInterval` (1.0 s) has elapsed, **and only inside the branch that runs right after a CAN frame was received**. If the bus is silent, it isn't sent.
- **Receiver action**: byte 0 ≠ 0 → cruise control off (`state.CCactive = false`). Byte 1 → `state.SafeState`, which forces target current and RPM to 0 in `ReadPot` and shows the safe-state icon.
- **New STM32**: not implemented.

### 0x176: lights / brake request, steering wheel → main board
Encoded in steering `sendESPCAN` (`CAN_ID_ESP_TX`). Decoded in old main `assignCAN2variable`. In the new HUST27, `sendDashboardCAN()` is commented out in `CANfunc.cpp` and the ID is **not passed** by the HUST27 filters.

| Byte | Content | Type | Values |
|---|---|---|---|
| 0 | Left indicator | uint8 | 0 / 1 |
| 1 | Right indicator | uint8 | 0 / 1 |
| 2 | Hazard | uint8 | 0 / 1 |
| 3 | Brake (`inputs.Brake != 0`) | uint8 | 0 / 1 |
| 4–7 | Unused | uint8 | 0x00 |

- **Period**: 100 ms (`ProcessDrivingCAN`).
- The steering wheel encodes bytes 0–2 with `if / else if / else if`, so **only one** of left, right and hazard is ever 1. Left wins over right, and right wins over hazard. That means the hazard bit is dropped whenever an indicator flag is also set. The inputs logic normally clears them, so in practice this is fine.
- Byte 3 is effectively **always 0** in the old code: brake pedal mapping is disabled (`mapFloat(..., 0, 0)` in `Inputs.cpp`, with the comment "BRAKE TURNT OFF").
- **Old-main bug**: `case 0x176` has no `break`, so it falls through into `case 0x501` and overwrites `driver_current` / `driverRPM` with the lamp bytes reinterpreted as floats.
- The commented-out HUST27 version writes left/right/hazard independently (no else-if) and sets byte 3 from `Brake != 0`. It isn't needed in 2027.

---

## Motor controller (Tritium WaveSculptor, GUESS)

### 0x501: motor drive command, driver controls → MC
Encoded in steering `sendDriveCAN(inputs.TargetRPM, inputs.TargetCurrent)` (`CAN_ID_DRIVE_CMD`). Decoded by the old main (logging only, with the fall-through bug above). In HUST27, `sendDriveCAN` is declared in `CANfunc.h` but the body is commented out in `CANfunc.cpp`.

| Bytes | Content | Type | Units / values |
|---|---|---|---|
| 0–3 | Motor velocity setpoint | float LE | rpm. Code uses 20000 (forward, current-limited "torque mode"), −100 (regen/brake), 0 (off) |
| 4–7 | Motor current setpoint | float LE | 0.0–1.0 = fraction of max current. Gas maps to 0..`GasLimiter`/5. The cruise PID output is clamped to 0..1 |

- **Period**: 100 ms. GUESS from spec: the WaveSculptor stops driving if it gets no command for about 250 ms. Verify.
- The layout matches the WaveSculptor "Motor Drive Command" at driver-controls base 0x500 + 1 (GUESS, from external spec knowledge).

### 0x401: MC status
Decoded in steering (`CAN_ID_MC_ERROR`) and HUST27: `MCerror = (buf[2] != 0)`. The old main doesn't decode it.

| Byte | Content per code | Per WaveSculptor spec (GUESS, from external spec knowledge) |
|---|---|---|
| 0–1 | unknown | Limit flags (uint16) |
| 2 | Error if ≠ 0 | Error flags, low byte |
| 3 | not read | Error flags, high byte. **Errors flagged only in byte 3 are missed** |
| 4–5 | unknown | Active motor index |
| 6 | unknown | CAN TX error count |
| 7 | unknown | CAN RX error count |

### 0x402: MC bus measurement

| Bytes | Content | Type | Units |
|---|---|---|---|
| 0–3 | DC bus voltage | float LE | V (steering: `motor.Voltage`; HUST27: commented out) |
| 4–7 | DC bus current | float LE | A (`motor_current` / `MotorCurrent`) |

The steering wheel shows motor power as `-1 * Current * Voltage`, so the sign convention is that negative current = drawing from the bus. **GUESS**.

### 0x403: MC velocity

| Bytes | Content | Type | Units |
|---|---|---|---|
| 0–3 | Motor speed | float LE | rpm (steering `motor.RPM`; HUST27 commented out) |
| 4–7 | Vehicle velocity | float LE | m/s. Steering and HUST27 multiply by 3.6 → km/h. **The old main stores it raw (m/s)** and logs and transmits it without converting |

### 0x40B: MC temperatures

| Bytes | Content | Type | Units |
|---|---|---|---|
| 0–3 | Motor temperature | float LE | °C |
| 4–7 | Heat-sink (controller) temperature | float LE | °C |

### 0x40E: MC odometer and bus amp-hours

| Bytes | Content | Type | Units |
|---|---|---|---|
| 0–3 | Odometer / distance since reset | float LE | Code labels and prints it as **km**. The WaveSculptor spec gives **metres** (GUESS, from external spec knowledge). Possible unit bug |
| 4–7 | DC bus amp-hours | float LE | Ah (steering `motor.Amps`. Not read by the old main or HUST27) |

The other IDs passed by the HUST27 MC filter (0x400, 0x404–0x40A, 0x40C, 0x40D, 0x40F) are **not decoded**. GUESS: per the WaveSculptor spec, 0x400 is the ID/serial frame and the rest are phase currents, voltage vector, rail voltages, fan speed, slip speed and similar.

---

## BMS (Orion BMS, custom message config)

### 0x601: BMS temperatures

| Byte | Content | Type | Units |
|---|---|---|---|
| 0 | unknown (not read) | — | — |
| 1 | BMS internal temperature | uint8 | °C |
| 2 | Highest cell temperature | uint8 | °C |
| 3 | Lowest cell temperature | uint8 | °C |
| 4 | Average cell temperature | uint8 | °C |
| 5 | ID of the hottest thermistor/cell | uint8 | index |
| 6 | ID of the coldest thermistor/cell | uint8 | index |
| 7 | unknown (not read) | — | — |

- All three decoders treat temperatures as **unsigned**, so sub-zero temperatures can't be represented. Whether the Orion field is signed is **unknown**.
- The old main names bytes 5/6 `battery_cell_ID_HIGH_volt` / `battery_cell_ID_LOW_volt`, but they are **temperature** IDs. HUST27 names them correctly (`CellHighTemperature_ID`).
- The steering wheel sets `bms.HighTemp` when byte 1 ≥ 50 or byte 2 ≥ 50. That 50 °C threshold is hard-coded.

### 0x602: BMS pack data

| Bytes | Content | Type | Scale | Units |
|---|---|---|---|---|
| 0–1 | Pack current | int16 BE | ×0.1 | A. Sign convention **GUESS**: the steering shows battery power as −I·V, so positive probably means discharge |
| 2–3 | Pack voltage | uint16 BE | ×0.1 | V |
| 4–5 | Lowest cell voltage | uint16 BE | ×0.0001 | V |
| 6–7 | Highest cell voltage | uint16 BE | ×0.0001 | V |

The old main also integrates `V·I·dt` into `BATTERY_WATTHOURS_SINCE_START` on every frame.

### 0x603: BMS average cell voltage

| Bytes | Content | Type | Scale | Units |
|---|---|---|---|---|
| 0–1 | Average cell voltage | uint16 BE | ×0.0001 | V |
| 2–7 | unknown (not read) | — | — | — |

### 0x605: BMS error flags

| Byte | Content |
|---|---|
| 0–5 | unknown (not read) |
| 6–7 | Fault flags. `BMSerror = (buf[6] != 0 \|\| buf[7] != 0)`. Individual bit meanings unknown (they depend on the Orion config) |

Decoded by the steering wheel and HUST27. The old main doesn't decode it.

The HUST27 BMS filter also passes **0x600, 0x604, 0x606 and 0x607**. Their content is **unknown** and they aren't decoded.

---

## MPPTs

### 0x200 / 0x210 / 0x220 / 0x230: MPPT 1–4 data
The MPPT index is `(ID − 0x200) / 0x10` (steering `CanHandler.cpp`).

| Bytes | Content | Type | Scale | Units |
|---|---|---|---|---|
| 0–1 | Input (array) voltage | uint16 BE | ×0.01 | V |
| 2–3 | Input (array) current | int16 BE | ×0.0005 | A |
| 4–5 | Output (battery-side) voltage | uint16 BE | ×0.01 | V |
| 6–7 | Output current | int16 BE | ×0.0005 | A |

- Output power = Vout × Iout. Total solar power = the sum over the MPPTs.
- **HUST27 handles only 0x200, 0x210 and 0x220.** 0x230 passes the filter but is ignored, and HUST27 doesn't decode input V/I.
- **Old-main bug**: the sign of Iout is decided from `data[2]` (the Iin MSB) instead of `data[6]`.
- The old main zeroes every MPPT power value if no MPPT frame arrives for 5 s. Neither the steering wheel nor HUST27 has a timeout.
- The other IDs in 0x201–0x23F (passed by the HUST27 filter) are **unknown**. GUESS: per-MPPT status or limit frames.

### 0x177: MPPT IV-sweep command
Reported by the team as used on the 2025 car. **Not found anywhere in the repo** (old or new code). Sender, period and payload are **unknown**.

---

## Filters in HUST27.ino (2027)

| Bank | ID | Mask | Passes | Missing for a full system |
|---|---|---|---|---|
| 0 | 0x400 | 0x7F0 | 0x400–0x40F (MC) | — |
| 1 | 0x600 | 0x7F8 | 0x600–0x607 (BMS) | — |
| 2 | 0x200 | 0x7C0 | 0x200–0x23F (MPPTs) | — |

Not passed: **0x175/0x176** (old steering-wheel link, no longer needed), **0x177** (IV sweep) and **0x501** (drive command; the main board transmits it, so it doesn't need to receive it).

## Implementation notes (current code)
- Every decoder reads floats with `*((float*)(buf + 4))`. That is unaligned type-punning: undefined behaviour, and on Cortex-M4F an FPU load (`VLDR`) from an unaligned address faults. Use `memcpy` into a `float` instead.
- The 16-bit fields are rebuilt in three different styles across the codebase (`(b0-256)*256+b1`, `(int16_t)(b0<<8|b1)`, and so on). They agree, except for the old-main MPPT sign bug noted above.

## Open questions
1. Which motor controller model and firmware is it (WaveSculptor 22?), and what is its configured base address? Please share its CAN spec so the GUESS rows can be confirmed.
2. Can you export the Orion BMS CAN message configuration (0x600–0x607)? It would pin down byte meanings, signedness, the current sign convention and the fault-flag bits.
3. Which MPPT model is it, and is there a full CAN spec (status frames, limits, and the 0x177 IV-sweep command)?
4. What is the 0x177 payload, and who sends it (pit command via LoRa? the main board?)?
5. ~~Will the steering wheel still be a separate CAN node?~~ **Answered: no.** One MCU, and the main board sends 0x501.
