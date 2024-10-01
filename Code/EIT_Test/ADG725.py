import spidev
import RPi.GPIO as GPIO

# Constants for ADG725 commands
ADG725_ALLOFF = 0x80
ADG725_A_ONLY = 0x20
ADG725_B_ONLY = 0x40

class ADG725:
    def __init__(self, spi_bus, spi_device, max_speed_hz=1000000, spi_mode=0b01):
        GPIO.setmode(GPIO.BCM)

        # Set the SPI bus and device from parameters
        self.spi = spidev.SpiDev(spi_bus, spi_device)
        
        # Configure SPI parameters
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = spi_mode

    def setChannel(self, channel):
        self.spi.xfer([channel & 0x0F])

    def setChannelA(self, channel):
        self.spi.xfer([ADG725_A_ONLY | (channel & 0x0F)])

    def setChannelB(self, channel):
        self.spi.xfer([ADG725_B_ONLY | (channel & 0x0F)])

    def allOff(self):
        self.spi.xfer([ADG725_ALLOFF])

    def setAll(self):
        for i in range(16):
            self.spi.xfer([i & 0x0F])

    def setAllA(self):
        for i in range(16):
            self.spi.xfer([ADG725_A_ONLY | (i & 0x0F)])

    def setAllB(self):
        for i in range(16):
            self.spi.xfer([ADG725_B_ONLY | (i & 0x0F)])

    def channelCount(self):
        return 16

    def close(self):
        """Close the SPI connection and cleanup GPIO."""
        self.spi.close()
        GPIO.cleanup()
