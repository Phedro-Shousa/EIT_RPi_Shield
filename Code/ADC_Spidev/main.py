import time
import rpi_ad7606 as adc

def main():
    adc_pins = {'standby':None, 'convsta':6, 'reset':5, 'busy':22, '1stData':None}
    adc1 = adc.AD7606_SPI(5, 'simultaneous', adc_pins)
    print("ADC Object Created \n")

    adc1.ADCreset()
    print("ADC Reset \n")
    
    r = adc1.ADCread()
    _ch = 1
    for _r in r:
        print(f"Channel {_ch}: {_r} volts. \n")
        _ch += 1
        time.sleep(1)

    adc1.ADCreset()
    print("ADC Reset \n")

    adc1.close()  # Close the SPI and cleanup GPIO

if __name__ == '__main__':
    main()
