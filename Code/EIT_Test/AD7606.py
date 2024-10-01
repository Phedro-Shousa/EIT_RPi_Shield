import spidev
import RPi.GPIO as GPIO

class AD7606_SPI:
    def __init__(self, inputRange, pins, dataFreq=1000000, returnRaw=False):
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
         # Factor for converting raw readings
        self.inputRange = inputRange
        self.xferFactor = inputRange / (2**15) 
        self.returnRaw = returnRaw
        # GPIO pin assignments
        self.p_convsta = pins['convsta']
        self.p_reset = pins['reset']
        self.p_busy = pins['busy']
        # Setup GPIO pins
        GPIO.setup(self.p_convsta, GPIO.OUT)
        GPIO.setup(self.p_reset, GPIO.OUT)
        GPIO.setup(self.p_busy, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Setup SPI using spidev
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # SPI bus 0, device 0
        self.spi.max_speed_hz = dataFreq  # Set SPI frequency
        self.spi.mode = 0  # SPI mode 0

    def _twosComp(self, value):
        """Convert a 16-bit unsigned value to signed (two's complement)."""
        if (value & (1 << 15)) != 0:
            value -= (1 << 16)
        return value

    def transferFunction(self, reading):
        """Apply two's complement and scale the reading."""
        return self.xferFactor * self._twosComp(reading)

    def ADCreset(self):
        """Reset the ADC by toggling the reset pin."""
        GPIO.output(self.p_reset, 1)
        GPIO.output(self.p_reset, 0)

    def ADCread(self, n):
        """Read `n` channels of data from SPI."""
        GPIO.output(self.p_convsta, 0)
        GPIO.output(self.p_convsta, 1)
        # Read n * 2 bytes from SPI (2 bytes per channel)
        data = self.spi.readbytes(n * 2)
        if self.returnRaw:
            return data
        else:
            # Extract the last channel (n-th) data from SPI response
            value = (data[(n * 2) - 2] << 8) | data[(n * 2) - 1]
            return self.transferFunction(value)

    def close(self):
        """Close the SPI and clean up GPIO."""
        self.spi.close()
        GPIO.cleanup()
