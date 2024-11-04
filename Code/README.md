# Code for EIT RPi Shield

This folder contains all the source code and scripts necessary to run the Electrical Impedance Tomography (EIT) Raspberry Pi Shield, which includes components like ADC interfacing, current sensing, multiplexing, and waveform generation.

### 1. `EIT_Test/`
This folder contains scripts for testing the entire EIT system.
- **AD7606.py**: Functions for interacting with the AD7606 ADC.
- **AD9833.py**: Code to control the AD9833 waveform generator.
- **ADG725.py**: Script for handling the ADG725 multiplexer.
- **main.py**: Main script to run EIT testing.
- **send_data.py**: Sends test data from the Raspberry Pi.
- **spi6-extended.dtbo**: SPI configuration for the test setup.

### 2. `ADC_AD7606/`
- **main.py**: Main script to run and initialize the ADC.
- **rpi_ad7606.py**: Supporting functions to handle the SPI communication between the Raspberry Pi and AD7606.

### 3. `Current_Sense/`
- **main.py**: Script to run current sensing using the MAX4376 current sense amplifier.
- **rpi_ad7606.py**: Functions for ADC (AD7606) interfacing.
- **spi6-extended.dtbo**: Device Tree Blob for configuring SPI6 interface.
- **spi6-extended.txt**: Configuration details for the SPI6.
- **Data_Results/**: Folder containing measurement results at different frequencies (1kHz to 1MHz).

### 4. `Mux/`
- **ADG725.py**: Script for initializing and using the multiplexer.
- **test.py**: Test script to verify multiplexer functionality.

### 5. `WavGen_AD9833/`
- **main.py**: Script for generating waveforms.
- **rpi_ad7606.py**: Helper functions to read waveform data using the AD7606.
- **spi6-extended.dtbo**: SPI6 interface configuration for waveform generation.
