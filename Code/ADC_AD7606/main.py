import time
import pigpio as pg
import rpi_ad7606 as adc


def main():
    adc_pins = {'standby':None, 'convsta':6, 'reset':5, 'busy':22, '1stData':None}
    adc1 = adc.AD7606_SPI(5,'simultaneous',adc_pins, dataFreq=20000000, returnRaw=False)
    print("ADC Object Created ")
    print(format(adc1.dataFreq, ","))
    
    adc1.ADCreset()
    print("ADC Reset \n")
    r = adc1.ADCread()
    _ch = 1
    for _r in r:
        print("Channel {n}: {v} volts. \n".format(n=_ch,v=_r))
        _ch += 1
        time.sleep(1)
    adc1.ADCreset()
    print("ADC  Reset \n")
                                                                                                                    


if __name__ == '__main__':
    main()
