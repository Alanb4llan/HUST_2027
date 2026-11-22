# Graph Report - HUST27  (2026-11-22)

## Corpus Check
- 54 files · ~53,256 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 1659 file(s) not represented in the graph (top: .kicad_mod 739, .lbr 56, .scr 42)

## Summary
- 627 nodes · 1513 edges · 49 communities (33 shown, 16 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 166 edges (avg confidence: 0.83)
- Token cost: 385,640 input · 0 output

## Community Hubs (Navigation)
- Riverdi EVE Coprocessor Cmds
- EVE GPU HAL Types
- Old Main ESP32 Sketch
- New STM32 Firmware & Display
- Old Steering Wheel Logic
- EVE App Common Helpers
- Steering Wheel Screens & Icons
- Team Guide & CAN Tips
- EVE HAL Utilities
- LoRa TX IO Board Nets
- LoRa RX Board Nets
- Safe State & E-stop Rules
- Main Harness J1 Signals
- Generic L476 Reference Image
- Battery & BMS Rules
- ADXL312 Datasheet
- SPI1 Bus Peripherals
- Indicators, Display & Speed Rules
- LoRa isoSPI Link (Main)
- CAN Bus Hardware
- Braking & Cruise Rules
- Lighting Rules
- Scrutineering Docs & Horn
- LoRa RX Schematic Parts
- Solar Array Isolation Rules
- LoRa TX Schematic Parts
- USB-C Interface
- Pack Sealing Rules
- DRL LED Board
- 3.3V Power Supply
- Brake Light Driver
- LSE 32.768k Crystal
- Right Indicator Driver
- High Voltage Definitions
- 12V Rail & Fuse F1
- BOOT0 Switch
- Reversing Rule
- DRL Netlist
- LoRa RX Netlist
- LoRa RX Antenna
- LoRa RX Buck
- LoRa 32 MHz Crystal
- LoRa TX Netlist
- Main PCB Netlist
- Fuse F2
- Fuse F3
- Fuse F4
- Empty Inputs List

## God Nodes (most connected - your core abstractions)
1. `Gpu_Copro_SendCmd()` - 95 edges
2. `Gpu_CoCmd_StartFunc()` - 94 edges
3. `Gpu_CoCmd_EndFunc()` - 94 edges
4. `U1 STM32L476RGTx MCU (LQFP-64)` - 31 edges
5. `App_Show_Logo()` - 20 edges
6. `Safe State` - 17 edges
7. `J1 main harness connector 5007620481` - 17 edges
8. `App_Common_Init()` - 16 edges
9. `Gpu_Hal_WaitCmdfifo_empty()` - 15 edges
10. `main_screen()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `loop()` --calls--> `drawScreen()`  [INFERRED]
  graphify-out/converted/ino/Display_ino.cpp → firmware/Display/Display.cpp
- `loop()` --calls--> `sendCAN2steeringWheel()`  [INFERRED]
  graphify-out/converted/ino/Mainkod_ino.cpp → old_code_esp32/Main_Ratt_Belgien26/Mainkod/Mainkod/CAN_functions.cpp
- `loop()` --calls--> `assignCAN2variable()`  [INFERRED]
  graphify-out/converted/ino/Mainkod_ino.cpp → old_code_esp32/Main_Ratt_Belgien26/Mainkod/Mainkod/CAN_functions.cpp
- `loop()` --calls--> `blinkLEDs()`  [INFERRED]
  graphify-out/converted/ino/Mainkod_ino.cpp → old_code_esp32/Main_Ratt_Belgien26/Mainkod/Mainkod/LED_functions.cpp
- `loop()` --calls--> `sendLoRaData()`  [INFERRED]
  graphify-out/converted/ino/Mainkod_ino.cpp → old_code_esp32/Main_Ratt_Belgien26/Mainkod/Mainkod/LoRa_functions.cpp

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Safe State Implementation Components** — graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_safe_state_driver_switch, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_external_emergency_isolation, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_galvanic_isolation_contactors, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_solar_collector_isolation_relay, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_fail_safe_activation, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_estop_loop [EXTRACTED 0.95]
- **Always-Visible Driver Display Items** — graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_speed_display, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_direction_indicators, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_hazard_warning, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_bms, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_rear_vision [EXTRACTED 0.90]
- **Mandatory Vehicle Lighting Set** — graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_stop_lamps, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_central_stop_lamp, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_direction_indicators, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_daytime_running_lamps, graphify_out_converted_2027_bwsc_event_regulations_v1_0_published_07052026_hazard_warning [EXTRACTED 0.95]
- **Peripherals sharing SPI1 bus with separate chip selects** — graphify_out_converted_ext_int_pinouts_wiring_spi1_bus, graphify_out_converted_ext_int_pinouts_wiring_lora_signals, graphify_out_converted_ext_int_pinouts_wiring_screen_signals, graphify_out_converted_ext_int_pinouts_wiring_sd_cs, graphify_out_converted_ext_int_pinouts_wiring_accelerometer [INFERRED 0.85]
- **BWSC event communications and tracking equipment** — graphify_out_converted_2027_bwsc_team_managers_guide_v1_published_07052026_uhf_radio, graphify_out_converted_2027_bwsc_team_managers_guide_v1_published_07052026_satellite_phone, graphify_out_converted_2027_bwsc_team_managers_guide_v1_published_07052026_data_logger, graphify_out_converted_2027_bwsc_team_managers_guide_v1_published_07052026_telemetry_rules [EXTRACTED 1.00]
- **Main board SPI1 bus shared devices** — graphify_out_converted_main_pcb_netlist_net_spi1_sck, graphify_out_converted_main_pcb_netlist_u2, graphify_out_converted_main_pcb_netlist_ic3, graphify_out_converted_main_pcb_netlist_j8, graphify_out_converted_main_pcb_netlist_j1 [EXTRACTED 1.00]
- **LoRa RX ESP32-SX1262-SD SPI** — graphify_out_converted_lora_rx_netlist_u5, graphify_out_converted_lora_rx_netlist_u2, graphify_out_converted_lora_rx_netlist_j4 [EXTRACTED 1.00]

## Communities (49 total, 16 thin omitted)

### Community 0 - "Riverdi EVE Coprocessor Cmds"
Cohesion: 0.09
Nodes (104): COUNT_ARGS(), Gpu_Hal_Context_t, Get_GpuClock(), Gpu_CoCmd_AnimDraw(), Gpu_CoCmd_AnimFrame(), Gpu_CoCmd_AnimStart(), Gpu_CoCmd_AnimStop(), Gpu_CoCmd_AnimXY() (+96 more)

### Community 1 - "EVE GPU HAL Types"
Cohesion: 0.09
Nodes (69): bool_t, Fifo_t, GPU_81X_GPIO_DRIVE_STRENGTH_T, GPU_81X_GPIO_GROUP_T, GPU_81X_PLL_FREQ_T, Gpu_HalInit_t, GPU_PLL_FREQ_T, GPU_PLL_SOURCE_T (+61 more)

### Community 2 - "Old Main ESP32 Sketch"
Cohesion: 0.07
Nodes (36): can_functions, esp32_twai_can, FS, loop(), prepareAndWrite2SD(), setup(), setupSD(), led_functions (+28 more)

### Community 3 - "New STM32 Firmware & Display"
Cohesion: 0.07
Nodes (25): adafruit_gfx, adafruit_ssd1306, arduino, CAN_message_t, canfunc, dht, display, drawLeft() (+17 more)

### Community 4 - "Old Steering Wheel Logic"
Cohesion: 0.08
Nodes (19): app_common, canhandler, cruisecontrol, dispfunctions, loop(), setup(), inputs, CanReadAll() (+11 more)

### Community 5 - "EVE App Common Helpers"
Cohesion: 0.12
Nodes (29): Flash_Cmd_Status_t, App_Calibrate_Screen(), App_Common_Close(), App_Flush_Co_Buffer(), App_Flush_Co_Buffer_nowait(), App_Flush_DL_Buffer(), App_Play_Sound(), App_Read_Tag() (+21 more)

### Community 6 - "Steering Wheel Screens & Icons"
Cohesion: 0.25
Nodes (28): main_screen(), start_screen(), App_WrDl_Buffer(), Gpu_Hal_Context_t, cruise_control_icon(), current_consume_icon(), draw_rect(), drawHeadlight() (+20 more)

### Community 7 - "Team Guide & CAN Tips"
Cohesion: 0.13
Nodes (24): CAN bus EMI robustness, setAutoBusOffRecovery(true), setIRQPriority(5, 0) CAN interrupt, Battery Officer role, Organiser data logger tracking box (p35, Reg 2.9), Dynamic Scrutineering (p28-29), 2027 BWSC Team Managers Guide V1, Satellite phone (p36, Reg 3.8.2) (+16 more)

### Community 8 - "EVE HAL Utilities"
Cohesion: 0.16
Nodes (10): eeprom, float_t, cal_average(), da(), polar(), polarxy(), qcos(), qsin() (+2 more)

### Community 9 - "LoRa TX IO Board Nets"
Cohesion: 0.15
Nodes (19): IC1 74LVC125A buffer, J2 RJ45 jack, J3 antenna connector, Net-(J3-In) antenna net, BUSY net, /IO/BUSY_C net, CS net, DIO0 net (+11 more)

### Community 10 - "LoRa RX Board Nets"
Cohesion: 0.21
Nodes (16): D2 DSL70 USB ESD diode, J1 USB-A plug, J4 microSD connector, BUSY net, CS net, CS_SD net, DIO1 net, DIO2 net (+8 more)

### Community 11 - "Safe State & E-stop Rules"
Cohesion: 0.16
Nodes (15): Capacitor Auto-Discharge to <60 V in 5 s, Data Logging and Tracking Device, E-stop Loop, Fail-safe Safe State Activation, Pack Positive and Negative Contactors, Packs in Safe State During Removal/Reinstall, PV 200 mm Live Wiring Rule, Two-way Voice Radio Communication (+7 more)

### Community 12 - "Main Harness J1 Signals"
Cohesion: 0.21
Nodes (15): J1 main harness connector 5007620481, BRAKE net, CC+OK_MODE net, GAS net, INDICATORS+HAZARDS net, L_IND net, L_IND_OUT net, NRST net (Net-(S5-COM_1)) net (+7 more)

### Community 13 - "Generic L476 Reference Image"
Cohesion: 0.16
Nodes (14): Reference STM32L476RG schematic (EasyEDA), Battery monitor signals BAT_MON_EN and BAT-V (ADC), Quectel BG96 modem (MODEM_RST, EN_PWR_BG), BG96 modem power enable circuit (Q4 SI2301, Q5 AO3400, EN_PWR_BG to BG-PWR), Decoupling capacitors C4-C7 100nF on +3V30, I2C bus SDA/SCK on PB14/PB13 with R1/R2 10K pull-ups to P-VCC, X1 32.768kHz crystal with C1/C2 4.3pF on PC14/PC15, Peripheral power enable circuit (Q1 NTR1P02T1G P-MOSFET, Q2 BC847ALT1G, EN_PWR to P-VCC) (+6 more)

### Community 14 - "Battery & BMS Rules"
Cohesion: 0.18
Nodes (12): Auxiliary Battery Exemption (RTC, data retention, TPMS, 10 kJ), Battery Officer, Automatic Battery Management System, Cell Operating Ranges (V, I, T), External Charger Requirements (RCD, isolation, auto-stop), Energy Capacity Limit (11 MJ / 55 MJ), Energy Storage System Incident Plan, Energy Storage Pack (+4 more)

### Community 15 - "ADXL312 Datasheet"
Cohesion: 0.20
Nodes (12): ADXL312 3-axis digital accelerometer, BW_RATE output data rate, DEVID register 0x00, ADXL312 datasheet (Rev C), FIFO (bypass/FIFO/stream/trigger), ADXL312 I2C interface, Interrupts INT1/INT2 (INT_ENABLE, INT_MAP), POWER_CTL measure mode (+4 more)

### Community 16 - "SPI1 Bus Peripherals"
Cohesion: 0.23
Nodes (12): IC3 WSEN-ISDS 6-axis IMU (accelerometer/gyro, SPI/I2C), J8 microSD card connector, LoRa_CS net, Net-(U1-PA6) (via R28) net, SD_CS net, SENS_ACC_CS net, SENS_ACC_INT0 net, SENS_ACC_INT1 net (+4 more)

### Community 17 - "Indicators, Display & Speed Rules"
Cohesion: 0.20
Nodes (11): Cruiser Class Recharging, Direction Indicators (90+-30 flashes/min), COTS Phone/Tablet Driver Display Power Rule, Hazard Warning Signal, Driver Instrumentation Always-Visible Items, Instrumentation Powered From Energy Storage System, Minimum Speed 60 km/h, Forward/Sideward Vision Without Electronic Aids (+3 more)

### Community 18 - "LoRa isoSPI Link (Main)"
Cohesion: 0.31
Nodes (10): IC1 74LVC125A quad buffer, J5 RJ45 8P8C jack (LoRa link), LoRa_BUSY net, /Outputs/LORA_BUSY_C net, LoRa_DIO0 net, /Outputs/LORA_DIO0_C net, LoRa_RST net, /Outputs/LORA_RST_C net (+2 more)

### Community 19 - "CAN Bus Hardware"
Cohesion: 0.36
Nodes (9): J2 CAN connector (WR-MPC3), J3 CAN connector (WR-MPC3), J4 Micro-Fit 6-pin connector, CAN_H net, CAN_L net, CAN_RX net, CAN_TX net, S1 DP3T slide switch (CAN select) (+1 more)

### Community 20 - "Braking & Cruise Rules"
Cohesion: 0.25
Nodes (8): Automatic Driving Deactivation Rule, Service and Secondary Braking Systems, Cruise Control Deactivation Rule, Dynamic Scrutineering, Parking Brake (20% grade), Regenerative Braking in Brake Tests, Stop Lamp Operation Rule (driving possible and brakes applied), Rear Stop Lamps

### Community 21 - "Lighting Rules"
Cohesion: 0.25
Nodes (8): Central Stop Lamp, Certifying Engineer, No Driving Between Sunset and Sunrise, Daytime Running Lamps, DRL Operation Rule (whenever driving possible), Lamp Compliance UNECE R148 / SAE-DOT, Lighting Requirements, 2027 BWSC Event Regulations

### Community 22 - "Scrutineering Docs & Horn"
Cohesion: 0.32
Nodes (8): Compulsory Documentation Groups A-E, Egress Within 15 Seconds, External Emergency Electrical Isolation Device, Audible Warning Device (Horn), High-Voltage Block Diagram, Top-view Diagram of Emergency Isolation Switches, Driver Safe State Activation Switch, Static Scrutineering

### Community 23 - "LoRa RX Schematic Parts"
Cohesion: 0.40
Nodes (6): LoRa-Rx schematic (4 pages), J1 USB connector, U1 BGS12P2L6E6327 RF switch, U2 SX1262, U4 LMR33630CDDA, U5 ESP32-S3-WROOM-1

### Community 24 - "Solar Array Isolation Rules"
Cohesion: 0.40
Nodes (5): Chassis Isolation Monitoring Device, Isolation Resistance 100 V ohm Limit, PV Rear Surface Live Assumption and Insulation, Solar Collector (6 m2 Challenger limit), Solar Collector Isolation Relay/Contactor

### Community 25 - "LoRa TX Schematic Parts"
Cohesion: 0.60
Nodes (5): LoRa-IO schematic (TX IO sheet), IC1 74LVC125A, J2 RJ45, U3 LTC6820, U5 74930000 transformer

### Community 26 - "USB-C Interface"
Cohesion: 0.50
Nodes (4): D3 DSL70 USB ESD/TVS diode, J7 USB-C connector, +5V rail, USB+ net

### Community 27 - "Pack Sealing Rules"
Cohesion: 0.67
Nodes (3): Challenger Pack Disconnect/Seal Window (19:15-06:15), Observer, Energy Storage Pack Tamper-Evident Sealing

### Community 28 - "DRL LED Board"
Cohesion: 1.00
Nodes (3): J1 screwless input connector, D1-D9 white LED 3x3 strings, R1-R3 current-limit resistors

### Community 29 - "3.3V Power Supply"
Cohesion: 0.67
Nodes (3): +3.3V rail, /Peripheral/VIN net, U5 Wurth LGA-12EP buck regulator (3.3V)

### Community 30 - "Brake Light Driver"
Cohesion: 0.67
Nodes (3): BRAKE_LIGHTS net, BRAKE_LIGHTS_OUT net, Q2 DMN3023L N-MOSFET (brake lights)

### Community 31 - "LSE 32.768k Crystal"
Cohesion: 0.67
Nodes (3): OSC_IN net, OSC_OUT net, Y1 32.768 kHz watch crystal

### Community 32 - "Right Indicator Driver"
Cohesion: 0.67
Nodes (3): R_IND net, R_IND_OUT net, Q3 DMN3023L N-MOSFET (right indicator)

## Ambiguous Edges - Review These
- `DRL Operation Rule (whenever driving possible)` → `No Driving Between Sunset and Sunrise`  [AMBIGUOUS]
  graphify-out/converted/2027-BWSC-Event-Regulations-V1.0-Published-07052026.txt · relation: conceptually_related_to

## Knowledge Gaps
- **80 isolated node(s):** `src`, `w`, `h`, `x0`, `y0` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 140 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `DRL Operation Rule (whenever driving possible)` and `No Driving Between Sunset and Sunrise`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Gpu_Copro_SendCmd()` connect `Riverdi EVE Coprocessor Cmds` to `EVE GPU HAL Types`, `EVE App Common Helpers`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **Why does `Gpu_CoCmd_EndFunc()` connect `Riverdi EVE Coprocessor Cmds` to `EVE GPU HAL Types`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `Gpu_CoCmd_StartFunc()` connect `Riverdi EVE Coprocessor Cmds` to `EVE GPU HAL Types`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Gpu_Copro_SendCmd()` (e.g. with `App_WrCoCmd_Buffer()` and `Gpu_Hal_Transfer32()`) actually correct?**
  _`Gpu_Copro_SendCmd()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Gpu_CoCmd_StartFunc()` (e.g. with `Gpu_Hal_CheckCmdBuffer()` and `Gpu_Hal_StartCmdTransfer()`) actually correct?**
  _`Gpu_CoCmd_StartFunc()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Gpu_CoCmd_EndFunc()` (e.g. with `Gpu_Hal_EndTransfer()` and `Gpu_Hal_Updatecmdfifo()`) actually correct?**
  _`Gpu_CoCmd_EndFunc()` has 2 INFERRED edges - model-reasoned connections that need verification._