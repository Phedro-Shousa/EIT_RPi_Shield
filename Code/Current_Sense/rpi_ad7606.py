import spidev
import RPi.GPIO as GPIO
from time import sleep
from numpy import zeros, int16

class AD7606_SPI:
    def __init__(self, inputRange, conversionABmode, pins, dataFreq=10000000, returnRaw=False):
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)
        
        self.inputRange = inputRange
        self.xferFactor = inputRange / (2**15)
        self.ABmode = None
        self.p_standby = pins['standby']
        self.p_convsta = pins['convsta']
        self.p_reset = pins['reset']
        self.p_busy = pins['busy']
        self.p_1stData = pins['1stData']
        self.returnRaw = returnRaw

        # Setup GPIO pins as output or input
        GPIO.setup(self.p_convsta, GPIO.OUT)
        GPIO.setup(self.p_reset, GPIO.OUT)
        GPIO.setup(self.p_busy, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Setup SPI using spidev
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Open SPI bus 0, device (chip select) 0
        self.spi.max_speed_hz = dataFreq  # Set SPI frequency
        self.spi.mode = 0  # SPI mode 0

    def transferFunction(self, reading):
        def _twosComp(_val):
            if (_val & (1 << 15)) != 0:
                _val = _val - (1 << 16)
            return _val
        return self.xferFactor * _twosComp(reading)

    def ADCreset(self):
        GPIO.output(self.p_reset, 1)
        GPIO.output(self.p_reset, 0)

    def ADCread(self, n):
        GPIO.output(self.p_convsta, 0)
        GPIO.output(self.p_convsta, 1)

        # Read 16 bytes from SPI
        data = self.spi.readbytes(n*2)
		
        if self.returnRaw:
            return data
        else:
            value = data[(n*2)-2] << 8 | data[(n*2)-1]
            return self.transferFunction(value)

    def close(self):
        # Clean up SPI and GPIO
        self.spi.close()
        GPIO.cleanup()
