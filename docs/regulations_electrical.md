# BWSC 2027 – requirements that affect electronics and firmware

**Source:** `regulations/2027-BWSC-Event-Regulations-V1.0-Published-07052026.pdf`, cited as §section, page N. The PDF was converted to text with pypdf. Every clause below was re-read in that text, and requirements are paraphrased. One non-regulation note comes from the Team Managers Guide V1 (marked TMG).

**Status key**
- **old** = implemented in the old ESP32 code
- **partly** = partly implemented
- **missing** = not implemented anywhere
- **HW** = hardware or outside firmware

"New" means `firmware/HUST27` and `firmware/Display`. Pin references are from [pin_map.md](pin_map.md).

> HUST's class (Challenger or Cruiser) isn't stated in the repo. Clauses that only apply to one class are marked.

---

## 1. Lighting (§2.23)

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 2.23.1 / p39 | Fit two rear stop lamps, one central stop lamp, L+R front, side and rear indicators, and two DRLs. Headlamps and tail lamps aren't required. | The main board has three low-side lamp outputs: L_IND (PA9→Q1), R_IND (PA8→Q3) and BRAKE_LIGHTS (PB3→Q2). The central stop lamp presumably shares the brake circuit. There is **no DRL output** on the main board, and the DRL board is passive (3×3 LEDs, 2-wire input). | partly / HW |
| 2.23.2 / p39 | Colours: stop lamps red, indicators amber, DRL white. | Lamp hardware only. | HW |
| 2.23.3 / p39–40 | Lamps must comply with UNECE R148 or SAE/DOT, shown by markings or photometric documentation. | The DRL board's LEDs need photometric proof if they're self-designed. | HW |
| 2.23.4 / p40 | Each position needs the correct lamp category (e.g. side indicators category 5/6, stop S1/S2, central S3, DRL RL). | Lamp selection. | HW |
| 2.23.11 / p41 | Indicators must flash at **90 ± 30 flashes/min** (60–120). | Old main: `blinkInterval = 333` ms toggle, so a 666 ms period, which is 90/min ✔. New `HUST27.ino` drives PA8/PA9 permanently HIGH ✘. `Display.ino` toggles at 500 ms (60/min), right at the lower limit. | old; **missing** in new |
| 2.23.12 / p42 | It must be possible to flash L and R together as hazard warning. | Old main blinks both on `hazard_light` or `safeState`. New: no hazard logic in HUST27 (only `Display.ino` UI state). | old; **missing** in new |
| 2.23.13 / p42 | DRL mounting: ≥600 mm apart (≥400 mm if car <1300 mm wide), ≥250 mm high, visibility 10° up/down, 20° in/out. | Mechanical. | HW |
| 2.23.15 / p42 | Stop lamps must light **whenever driving is possible and the brakes are applied**. | Should be a **local path**: BRAKE input PB1 → BRAKE_LIGHTS PB3, independent of CAN and of the display MCU. Old main used CAN 0x176 byte 3 OR a hardware brake-switch pin, with PWM 255 for brake and 64 for tail. New HUST27 drives **PA10** (that's LoRa_DIO0, the wrong pin) constantly HIGH. Note: the old steering wheel had pedal brake mapping disabled (`mapFloat(...,0,0)`). | old; **missing** in new |
| 2.23.16 / p42 | DRLs must operate **whenever driving is possible**. | Old main set the DRL pin HIGH permanently. Nothing on the new main board drives DRLs, so they're presumably switched with vehicle power. → open question. | **missing** / HW? |
| 3.24.8 / p59 | No driving on public roads between sunset and sunrise. | This is why headlamps aren't required (see the 2.23.1 note). | info |

## 2. Horn (§2.24)

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 2.24.1 / p42 | Fit an automotive horn (or pair) complying with UNECE R28, clearly audible outside. | No horn net on the main board and no horn input in any code (the old main declared an unused `int horn`). Spare J1 GPIOs exist (PB10–PB15, PC8–PC12…). → open question. | **missing** |

## 3. Driver instrumentation (§2.25) and display power (§2.5.9)

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 2.25.1 / p42 | While moving, these must **always be visible (not behind menus)**: speed, indicator status, hazard status, **energy storage warnings**, and electronic rear-vision images (if fitted). | Old steering wheel `main_screen()` shows km/h, turn icons (both for hazard), and BMS-error and high-temp icons ✔. `Display.ino` shows speed and arrows, but prints "TEST TEST" for hazard and has no ESS warnings. 2027 display: an **OLED** on SPI1 via J1 (model not chosen yet). With a small screen, these items get priority on the main page. A distinct hazard indicator is advisable. | old; partly in new |
| 2.25.2 / p42 | That instrumentation must be powered from the energy storage system, **not separate batteries**. | Display powered from car 12 V via J1 / main board ✔. USB power is for bench use only. | HW |
| 2.5.9 / p25 | If a COTS phone/tablet is the driver display: power it from the car, block reverse current with a diode **within 200 mm** of the device, don't charge it externally during the event, and its battery counts toward ESS capacity. | Only relevant if a phone/tablet display is chosen. | HW (if used) |

## 4. Automatic functions (§2.26)

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 2.26.1 / p43 | Cruise control must **auto-deactivate when the brake is operated or the car is turned off**, and must **not resume automatically** after braking. | Old steering wheel: CC cancels when `inputs.Brake != 0` (but the pedal mapping was forced to 0), or when CAN 0x175 byte 0 (main-board brake switch) ≠ 0, or when Drive is off or in safe state. CC only re-engages on a deliberate CC-down press ✔, and CC is false at power-up ✔. The brake cancel therefore depended on CAN from the main board. Implement the cancel locally from BRAKE (PB1) on whichever MCU runs CC. | partly (old); **missing** in new |
| 2.26.2 / p43 | Any automatic driving function must deactivate immediately on manual input or power-off, with no auto-resume. | No such function exists. | N/A |

## 5. Energy storage / BMS (§2.5)

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 2.5.2 / p23–24 | ESS capacity ≤ **11 MJ** (Challenger) / ≤ 55 MJ (Cruiser), computed from manufacturer cell data. | Informational. The old main integrated `BATTERY_WATTHOURS_SINCE_START` from 0x602, which is useful for telemetry. | info |
| 2.5.5 / p24 | Cells must never be operated outside the manufacturer's V, I and T ranges. Specs must be supplied. | BMS (Orion-style IDs 0x600–0x607). Firmware only reads and displays it. | HW |
| 2.5.6 / p24 | The car must **automatically** prevent out-of-range operation (BMS), endorsed by the certifying engineer. | The BMS hardware does this. Firmware shows `BMSerror` (0x605 bytes 6–7) and `HighTemp`, and must never be the protection mechanism. | HW (display: old) |
| 2.5.7 / p24–25 | Batteries used only for an RTC, data retention or wireless TPMS aren't part of the ESS if the total is ≤ **10 kJ**. | VBAT is tied to +3.3 V (no RTC backup cell). Adding a coin cell for the RTC would be allowed. | info |
| 2.5.10 / p25 | Capacitors aren't counted as ESS if total < 36 kJ. | — | info |
| 2.5.11 / p25 | Capacitors outside packs or the solar collector must discharge to **< 60 V within 5 s** of safe state. | Main-board caps are low voltage. This applies to the motor controller and MPPT HV side. | HW |
| 2.5.16 / p26 | Packs must be in safe state while being removed or reinstalled. | — | HW |
| 2.5.18 / p26 | External chargers: use an RCD, isolated output, approved connection, and **charging must stop automatically when full or on fault**. | Charger and BMS interlock. Firmware isn't involved unless it controls charging (not planned). | HW |

## 6. Electrical safety (§2.27)

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 2.27 / p43 | "High voltage" means > 60 V dc or > 30 V rms ac. Based on UNECE R100 §5. | The main board is a 12 V / 3.3 V low-voltage system. | info |
| 2.27.7–2.27.8 / p44 | Isolation from exposed conductive parts must be > **100 Ω per volt** (ESS nominal voltage, and solar-collector max voltage). | — | HW |
| 2.27.9 / p44 | Isolation must be monitored by a **permanently connected electronic device**. | An isolation monitor (IMD) is required. If it has CAN or a status output, firmware could display or log it. The repo doesn't say which device. → open question. | HW / unknown |
| 2.27.10 / p44 | Each pack needs a fuse or breaker rated for the wiring, with adequate DC interrupt rating. | — | HW |

## 7. Safe state (§2.28)

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 2.28.1 / p44–45 | In safe state: contactors on **both** poles of every pack open; no voltage out of packs or solar collector (a relay or contactor on the same structure as the array, unless <200 mm of live wire); all contactors open immediately and automatically; no current in external loops. **MOSFETs don't count as galvanic isolation.** A separate "standby" state is allowed. | The main board's MOSFET lamp drivers are not isolation devices. | HW |
| 2.28.2 / p45 | Conductors > 200 mm from the nearest PV cell are outside the solar collector. | — | HW |
| 2.28.3 / p45 | All safe-state mechanisms must be **fail-safe**: on activation failure the car enters safe state and stays there until deliberate team intervention. | Firmware must not be in the activation path. | HW |
| 2.28.4 / p45 | The safe-state circuit must be simple, and **no semiconductor failure** may prevent entering it or release it without deliberate driver action. | → **The MCU must never be required to enter, hold or leave safe state.** It may only *sense* it, for display, hazard flashing and telemetry. Old main sensed `READ_SAFE_STATE`, flashed indicators and the safe-state light, and sent CAN 0x175 byte 1. **The new main board has no safe-state sense net** → open question. | HW; sense **missing** in new |
| 2.28.5 / p45 | The driver can enter safe state with one simple action, belted, from the driving position. The switch must be labelled. | — | HW |
| 2.28.6 / p45–46 | An exterior one-action switch inside a 180 mm yellow disc (blue triangle, red flash, "Emergency Electrical Isolation"), within 100 mm of the windscreen's lower edge by the egress. Repeated presses must not exit safe state. | — | HW |

## 8. Braking, driving, steering, vision

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 2.20.2–2.20.3 / p37 | Service brake operated without removing hands from the steering control. A secondary system on the same control must work after a single failure. | Mechanical/hydraulic. Firmware-controlled regen is not a substitute. | HW |
| 2.20.9 / p38 | Service-brake stopping distance is tested **with minimum regen**. If regen is disabled when the ESS is full, the test is done with **no** regen. | Regen comes from the drive command (old: `TargetRPM = -100` plus a current from the brake pedal, but pedal mapping was disabled). Regen behaviour must be predictable and switchable for testing. | info |
| 2.22.2 / p39 | The car must be able to **reverse under its own power**, driver seated normally. | No reverse command in old code (only positive RPM, or −100 for regen). Unclear whether the MC handles direction in hardware. The new board has a NEUTRAL input (PC5). → open question. | **missing?** |
| 2.18.2 / p35 | Failure of any non-mechanical steering component must not prevent effective steering. | Steering-wheel electronics (buttons, display) must be mechanically independent of steering. | HW |
| 2.16.3 / p34 | Forward and sideward vision must not rely on mirrors, lenses or **electronic vision systems**. | No camera may be used for forward vision. | HW |
| 2.17.2 / p35 | Rear vision may be electronic and/or mirrors. Driving must be impossible without effective rear vision. Images must be upright and not mirrored left-right. | If a rear camera is used, its image must always be on screen (§2.25.1) with correct orientation, and the car shouldn't be drivable without it. | HW / display |

## 9. Tracker, telemetry, communication

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 2.9.1 / p28 | Provide space for the organiser's **self-powered** tracker (120×120×70 mm, ≤ 2 kg). No electrical connection is needed. | No firmware interface. | HW |
| 2.9.2 / p28 | A 120° cone above the tracker top face must be **radio-transparent for 300–3000 MHz** (no carbon, metal or solar cells). | Affects tracker and LoRa antenna placement. The 915 MHz LoRa antenna and metal should stay out of that cone. | HW |
| 3.22.1 / p58 | The car carries the organiser's data logging and tracking device (spec in §2.9). | TMG p35: the box is fitted at scrutineering. | HW |
| 3.8.1 / p49 | Two-way **voice** radio to the rear escort must work whenever the driver is in the car, **including with contactors open / in safe state**. | Its radio power must not depend on the main contactors. Separate from LoRa telemetry. | HW |
| TMG p35–36 (not a regulation) | Radio use must comply with Australian law. ACMA's main concern is interference with licensed users, and out-of-band equipment may be swamped. Pick a frequency that is in-band and interference-free. | The car LoRa module is **RFM95W-915S2** (915 MHz), but `LoRafunc.cpp` and the old code use `LoRa.begin(868E6)`. Use the Australian 915–928 MHz band (the old code's own comment says so). | **mismatch** |

## 10. Documentation and scrutineering

| § / page | Requirement | HUST27 impact | Status |
|---|---|---|---|
| 1.29.1 / p18 | Group B (**due 5 March 2027**) includes the *Electrical System Specification* and *Energy Storage System Specification*. Group C (30 April 2027) includes the ESS Incident Plan. | The firmware/electronics description (pin map, CAN protocol) feeds the Electrical System Specification. | docs |
| 1.29.1 / p19 | At Static Scrutineering bring printed copies of: the top-view diagram with the emergency isolation switches; the single-sheet HV block diagram; and a simplified **safe-state electrical diagram** showing the e-stop loop, contactor control, LV bus de-energising and battery fuses. | — | docs |
| 3.12.6 / p52 | Road-ready checks include **lights, indicators and horn** and electrical compliance. | A scrutineering test mode (cycle all lamps and horn on command) would help. | **missing** |
| 3.28.8–3.28.9 / p62 | *(Challenger)* Packs disconnected and sealed **before 19:15**, not unsealed before 06:15. | The main board loses power overnight unless it has an aux supply. SD logging must survive power loss (flush and close often), and the RTC loses time (VBAT on the 3.3 V rail). | design constraint |

---

## Checklist

| Item | § | Where it belongs | Old code | New code |
|---|---|---|---|---|
| Indicators flash 60–120/min (target 90) | 2.23.11 | Main board PA8/PA9 | ✔ (333 ms) | ✘ (always on) |
| Hazard = both indicators | 2.23.12 | Main board | ✔ | ✘ |
| Stop lamps on brake, independent of CAN | 2.23.15 | Main board PB1 → PB3 | ✔ (CAN + pin) | ✘ (wrong pin PA10) |
| DRL on whenever driving possible | 2.23.16 | ? (no main-board net) | ✔ (pin HIGH) | ✘ / HW? |
| Horn | 2.24.1 | ? (no net) | ✘ | ✘ |
| Speed, indicators, hazard, ESS warnings always visible | 2.25.1 | Driver display | ✔ (EVE) | partly (test sketch) |
| Display powered from ESS | 2.25.2 | HW | ✔ | ✔ (12 V) |
| Cruise cancels on brake / power-off, no auto-resume | 2.26.1 | MCU running CC | partly (CAN-dependent) | ✘ |
| BMS warnings shown and logged | 2.5.6, 2.25.1 | Display / telemetry | ✔ | partly (decoded, not shown) |
| Safe state only sensed, never controlled by MCU | 2.28.3–2.28.4 | HW + sense input | ✔ (sense pin) | ✘ (no sense net) |
| Reverse under own power | 2.22.2 | MC / drive command | ✘ | ✘ |
| Telemetry on an Australian in-band frequency (915 MHz) | TMG p36 | LoRa | ✘ (868 MHz) | ✘ (868 MHz) |
| Lamp/horn test mode for scrutineering | 3.12.6 | Main board | ✘ | ✘ |
| Logging survives overnight power-off | 3.28.8 | SD logger | partly | ✘ |

## Open questions
1. Is HUST entering the **Challenger** or **Cruiser** class? (This affects 2.5.2 and 3.28.8–3.28.9.)
2. Where are the **horn** and **DRL** switched? Neither has a net on the main board, and the DRL board is passive.
3. How will the main board **sense safe state** for display, hazards and telemetry? The old car used a dedicated input, and the new schematic has none.
4. Which **isolation monitoring device** (2.27.9) is used, and does it report over CAN?
5. How is **reverse** (2.22.2) done: an MC direction input, or a negative velocity setpoint in the drive command?
6. Is a **rear-view camera** planned? If so, it must be permanently on the driver display (2.17.2, 2.25.1).
7. Confirm the telemetry frequency (915–928 MHz) and that the pit receiver (SX1262 on `lora_rx`) is set up to match.
