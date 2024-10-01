import spidev
import RPi.GPIO as GPIO

class AD9833:
    def __init__(self, bus, device, clock_freq=25000000):
        """Initialize the AD9833 wave generator"""
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0b10
        self.clock_freq = clock_freq
        self.freq = 10000000  # Default frequency

    def reset(self):
        """Send a reset command to the AD9833"""
        self.spi.xfer([0x21, 0x00])  # Reset 0x2100

    def set_frequency(self, freq):
        """Set the frequency for the AD9833 wave generator"""
        self.freq = freq
        # Calculate frequency word
        freq_word = int(round((self.freq * 2**28) / self.clock_freq))
        MSB = (freq_word & 0xFFFC000) >> 14
        LSB = freq_word & 0x3FFF
        # Set control bits DB15 = 0 and DB14 = 1 for frequency register 0
        MSB |= 0x4000
        LSB |= 0x4000
        # Send frequency LSB and MSB
        high, low = divmod(LSB, 0x100)
        self.spi.xfer([high, low])  # LSB
        high, low = divmod(MSB, 0x100)
        self.spi.xfer([high, low])  # MSB

    def set_phase(self):
        """Set the phase to 0°"""
        self.spi.xfer([0xC0, 0x00])  # MSB

    def set_waveform(self, waveform):
        """Set the waveform for the AD9833 (sine, square, etc.)"""
        if waveform == 'sine':
            self.spi.xfer([0x00, 0x00])  # Sine wave
        else:
            # todo: implement other waveforms
            print("Invalid waveform")


    def close(self):
        """Close the SPI connection and cleanup GPIO"""
        self.spi.close()
        GPIO.cleanup()
