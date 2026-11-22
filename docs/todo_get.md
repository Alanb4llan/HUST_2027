# To get: datasheets, boards and parts for firmware work

Things the firmware team needs to get hold of. The order is roughly when we need them (see the porting order in [port_plan.md](port_plan.md)).

## Datasheets and specs

- [ ] **WSEN-ISDS IMU datasheet / user manual** (Würth 2536030320001). Needed for the IMU driver that cruise control uses. *Needed soon.*
- [ ] **OLED display datasheet** (controller IC, interface, resolution). First **choose the OLED model**. It should be SPI (CS/DC/RST), because that's what the main board has.
- [ ] **Motor controller CAN spec**. Confirm the model (Tritium WaveSculptor 22?), the base address, and the command timeout.
- [ ] **Orion BMS CAN message config** (export from the Orion utility). It gives the meanings of 0x600–0x607, signed/unsigned temperatures and the fault bits.
- [ ] **MPPT model and CAN spec**, including the 0x177 IV-sweep command payload.
- [ ] *(Only if LoRa misbehaves)* **LTC6820 datasheet**, for the max SPI clock over isoSPI.

## Boards

- [ ] **Assembled main board** (STM32L476RG). If it isn't ready yet, a **Nucleo-L476RG** (same MCU) works for early development.
- [ ] **LoRa TX board** (`lora_tx`, RFM95W-915) for the car.
- [ ] **LoRa RX board** (`lora_rx`, ESP32-S3 + SX1262) for the pit side.
- [ ] **DRL board**, for testing lights only.

## Parts and tools for the bench

- [ ] **ST-LINK programmer** (or a Nucleo's built-in ST-LINK) plus a cable to the main board's SWD pins (SWDIO PA13 = J1.E1, SWCLK PA14 = J1.E3, plus GND and 3.3 V).
- [ ] **USB-C cable**, for USB Serial (CDC) debugging.
- [ ] **12 V bench power supply**.
- [ ] **USB-CAN adapter**, to watch the bus and fake motor controller, BMS and MPPT messages on the desk. Plus a **120 Ω terminator**.
- [ ] **Mating connector and crimp pins for J1** (Molex 500762-0481 harness connector), to wire up inputs and lamps.
- [ ] **RJ45 (8P8C) cable**, main board J5 ↔ LoRa TX board. The two boards use the same pin order, so a straight-through cable should work.
- [ ] **Two 915 MHz antennas** (the TX board antenna connector is a Würth 60312202114509, so check what plugs into it).
- [ ] **microSD card**, for the logging tests.
- [ ] **The chosen OLED display**.
- [ ] **Test inputs**: 2 potentiometers (gas, brake) and buttons/switches for neutral, CC/OK and indicators/hazard. Check the voltage first: GAS on PB0 is only 3.6 V tolerant.
- [ ] **Test lamps**: 3 small 12 V lamps or LED modules (left, right, brake) for the output drivers.

## Answers to get

- [ ] **Hardware team:** where are the **horn**, **DRL** switching and a **safe-state signal** to the MCU handled? None of them is on the main board.
