# drl netlist (exported with kicad-cli from hardware/drl)

## Components
- D1: value=3030_158303250A footprint=LED_SMD_Wurth:D_Wurth_WL-SWTP-3030 sheet=/ desc=White Top view PLCC
- D2: value=3030_158303250A footprint=LED_SMD_Wurth:D_Wurth_WL-SWTP-3030 sheet=/ desc=White Top view PLCC
- D3: value=3030_158303250A footprint=LED_SMD_Wurth:D_Wurth_WL-SWTP-3030 sheet=/ desc=White Top view PLCC
- D4: value=3030_158303250A footprint=LED_SMD_Wurth:D_Wurth_WL-SWTP-3030 sheet=/ desc=White Top view PLCC
- D5: value=3030_158303250A footprint=LED_SMD_Wurth:D_Wurth_WL-SWTP-3030 sheet=/ desc=White Top view PLCC
- D6: value=3030_158303250A footprint=LED_SMD_Wurth:D_Wurth_WL-SWTP-3030 sheet=/ desc=White Top view PLCC
- D7: value=3030_158303250A footprint=LED_SMD_Wurth:D_Wurth_WL-SWTP-3030 sheet=/ desc=White Top view PLCC
- D8: value=3030_158303250A footprint=LED_SMD_Wurth:D_Wurth_WL-SWTP-3030 sheet=/ desc=White Top view PLCC
- D9: value=3030_158303250A footprint=LED_SMD_Wurth:D_Wurth_WL-SWTP-3030 sheet=/ desc=White Top view PLCC
- J1: value=691409320002 footprint=Connector_THT_Wurth:J_Wurth_WR-TBL_691409320002 sheet=/ desc=Series 4093 - Screwless Push In 3.81mm pitch - 45° cable entry - THT
- R1: value=R footprint=Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder sheet=/ desc=Resistor
- R2: value=R footprint=Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder sheet=/ desc=Resistor
- R3: value=R footprint=Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder sheet=/ desc=Resistor

## Nets (ref.pin[pinfunction/pintype])
- GND: D7.1[-_1/passive], D8.1[-_1/passive], D9.1[-_1/passive], J1.2[2_2/passive], J1.M2[M2_M2/passive]
- Net-(D1-+): D1.2[+_2/passive], R1.2[passive]
- Net-(D1--): D1.1[-_1/passive], D4.2[+_2/passive]
- Net-(D2-+): D2.2[+_2/passive], R2.2[passive]
- Net-(D2--): D2.1[-_1/passive], D5.2[+_2/passive]
- Net-(D3-+): D3.2[+_2/passive], R3.2[passive]
- Net-(D3--): D3.1[-_1/passive], D6.2[+_2/passive]
- Net-(D4--): D4.1[-_1/passive], D7.2[+_2/passive]
- Net-(D5--): D5.1[-_1/passive], D8.2[+_2/passive]
- Net-(D6--): D6.1[-_1/passive], D9.2[+_2/passive]
- Net-(J1-Pad1): J1.1[1_1/passive], J1.M1[M1_M1/passive], R1.1[passive], R2.1[passive], R3.1[passive]