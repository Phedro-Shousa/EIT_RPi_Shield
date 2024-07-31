# EIT_RPi_Shield: Electrical Impedance Tomography (EIT) Shield for Structural Health Monitoring (SHM)

# ONGOING. NOT TESTED!
## Overview

This project is an Electrical Impedance Tomography (EIT) shield system designed for Structural Health Monitoring (SHM). This shield is an educational device that allows you to "plug-and-play" and actively collect data using a Raspberry Pi.

## Hardware Setup

The hardware setup consists of:
- 16 electrodes
- 1 High-Speed ADC
- Amplitude and Phase Detector
- 2 Multiplexers (Mux)
- Wave Generator

The shield is powered by the Raspberry Pi's 5V supply, with added protection. In addition to these sensors, this shield has extra free pinouts from the ADC analog inputs and the Raspberry Pi, allowing for the testing of other sensors and components.

## Project Status

This is the first stage of a work in progress, with the PCB design currently concluded. Future improvements and code will be developed in the future. This project belongs to the Würzburg University Luft- und Raumfahrtinformatik department.

**Note:** This shield is not recommended for medical use or for use on people, as it does not comply with current health regulations. It is intended only for SHM use on objects.

## Electrical Specifications

| Component           | Specification                                                  |
|---------------------|----------------------------------------------------------------|
| Power Supply        | 5V (from Raspberry Pi)                                         |
| Electrodes          | - 16 Electrodes                                                |
|                     | - 5 free ADC channels                                          |
| ADC                 | - Input range ±5V or ±10V                                      |
|                     | - 16-bit 20KSPS                                                |
| Phase-Gain Detector | - Up to signals of 2.7GHz                                      |
|                     | - Gain scale of 30mV/dB                                        |
|                     | - Phase scale of 10mV/degree                                   |
| Wave Generator      | - Output signal up to 12MHz                                    |
|                     | - Serial CLK up to 40MHz                                       |
|                     | - Output signal voltage: Max 4.9V (load of 100Ω) or 4.5V (1kΩ) |
|                     | - Output signal voltage: Min 0.4V                              |
| MUX                 | - 4Ω on resistance                                             |
|                     | - Rail-to-rail                                                 |
|                     | - Serial CLK up to 30MHz                                       |


## Pictures
### Board

### Schematic
<img src="https://github.com/Phedro-Shousa/EIT_RPi_Shield/blob/main/PCB%20Design/Schematic.png" alt="Schematic Picture" width="800">

### PCB Layout
<img src="https://github.com/Phedro-Shousa/EIT_RPi_Shield/blob/main/PCB%20Design/PCB.png" alt="Schematic Picture" width="500">

---
