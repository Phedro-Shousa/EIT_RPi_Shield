import time
import AD7606 as adc
import ADG725 as mux
import AD9833 as wg
import send_data

V_AMP = 1
V_PHASE = 2
CUR_SEN = 3

def init_ADC():
    adc_pins = {'convsta':6, 'reset':5, 'busy':22}
    adc1 = adc.AD7606_SPI(5, adc_pins)
    print("ADC Object Created \n")
    print("ADC Reset \n")
    adc1.ADCreset()
    return adc1

def init_mux():
    mux_in = mux.ADG725(spi_bus=6, spi_device=0)
    mux_out = mux.ADG725(spi_bus=6, spi_device=3)
    print("Mux Init \n")
    mux_in.allOff()
    mux_out.allOff()
    print("Mux All Pins Off \n")
    return mux_in, mux_out

def init_wg():
    wg1 = wg.AD9833(bus=6, device=2)
    print("WG Init \n")
    wg1.reset()
    print("WG Reset \n")
    return wg1

def close_devices(adc1, mux_in, mux_out, wg1):
    adc1.close()  # Close the SPI and cleanup GPIO
    mux_in.close()
    mux_out.close()
    wg1.close()
  
def start_wg(wg1):
    wg1.set_frequency(1000)
    wg1.set_phase()
    wg1.set_waveform('sine')

def start_mux(mux_in, mux_out):
    mux_in.setChannelA(0)
    mux_in.setChannelB(1)
    mux_out.setChannelA(2)
    mux_out.setChannelB(3)

def read_current(adc1):
    samples = 1024
    max_value = 0      # lowest possible value
    min_value = 5000   # highest possible value 
    while samples > 0:
        r = adc1.ADCread(CUR_SEN)  # Read ADC value from the specified channel
        # Update the max and min values
        if r > max_value:
            max_value = r
        if r < min_value:
            min_value = r
        samples -= 1
    
    peak_peak_current = (max_value - min_value)
    avg_current = (max_value + min_value) / 2  # Example of avg current calculation
    

    print(f"Max Current: {(max_value/200):.2f} mA {max_value:.2f}\n")
    print(f"Min Current: {(min_value/200):.2f} mA {min_value:.2f}\n")
    print(f"Peak-Peak Current: {(peak_peak_current/200):.2f} mA {peak_peak_current:.2f}\n")
    print(f"Average Current: {(avg_current/200):.2f} mA {avg_current:.2f}\n")

    return max_value, min_value, peak_peak_current, avg_current

def EIT_read(adc1, mux_in, mux_out):
    num_channels = 16
    amp = []
    phase = []
    for i in range(num_channels):
        # Set current injection electrodes
        mux_in.setChannelA(i)
        mux_in.setChannelB((i + 1) % num_channels)
        # Read voltages from other electrodes
        for j in range(2, num_channels - 1):
            mux_out.setChannelA((i + j) % num_channels)
            # Read phase
            mux_out.setChannelB(i)
            phase.append(adc1.ADCread(V_PHASE))
            # Read the ADC amplitude
            mux_out.setChannelB((i + j + 1) % num_channels)
            amp.append(adc1.ADCread(V_AMP))

    # Return collected data 
    return amp, phase

def main():

    adc1 = init_ADC()
    mux_in, mux_out = init_mux()
    wg1 = init_wg()

    start_wg(wg1)
    start_mux(mux_in, mux_out)
    start = time.time()
    max_value, min_value, peak_peak_current, avg_current = read_current(adc1)
    end = time.time()
    result = (end - start)*1000
    print(f"EIT TIME: {result:.2f} ms")
    wg1.set_frequency(3000)

    # Start EIT data collection
    amp, phase = EIT_read(adc1, mux_in, mux_out)
    send_data.save_to_txt(amp, phase, max_value, min_value, peak_peak_current, avg_current)
    send_data.transfer_file()

    close_devices(adc1, mux_in, mux_out, wg1)


if __name__ == '__main__':
    main()
