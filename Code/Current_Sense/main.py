import spidev
import RPi.GPIO as GPIO
import keyboard  # To detect keypresses
import rpi_ad7606 as adc
import time
import subprocess

def write_data_to_file(data, filename="/home/pedro/Desktop/log.txt"):
    # Write the data to a temporary file on Raspberry Pi
    with open(filename, 'w') as f:
        f.write(data)


def transfer_file_to_laptop(filename):
    # SSH details
    user = "Pedro Sousa"  # Replace with your laptop's username
    ip = "132.187.210.53"  # Replace with your laptop's IP address

    # Correct the file path on Windows laptop with double backslashes and quotes
    destination_path = r"C:\\Users\\Pedro Sousa\\Desktop\\TOMOPLEX\\Redesign\\code\\log.txt"

    # Use scp to transfer the file to the laptop
    command = f"scp {filename} \"{user}@{ip}:{destination_path}\""
    
    # Execute the scp command to transfer the file
    subprocess.run(command, shell=True)

def main():
    freq = 1000000
    ClockFreq = 25000000
    
    print("Wav_Gem Test \n")
    GPIO.setmode(GPIO.BCM)
    spi = spidev.SpiDev(6, 2)
    spi.max_speed_hz = 10000000 
    spi.mode = 0b10
            
    adc_pins = {'standby':None, 'convsta':6, 'reset':5, 'busy':22, '1stData':None}
    adc1 = adc.AD7606_SPI(5, 'simultaneous', adc_pins)
    print("ADC Object Created \n")
    adc1.ADCreset()
    print("ADC Reset \n")
    
    # Send a reset
    spi.xfer([0x21, 0x00]) 
    print("Reset 0x2100 \n")
    
    # Calculate frequency word to send
    word = hex(int(round((freq * 2**28) / ClockFreq)))
    
    # Split frequency word onto its separate bytes
    MSB = (int(word, 16) & 0xFFFC000) >> 14
    LSB = int(word, 16) & 0x3FFF
    
    # Set control bits DB15 = 0 and DB14 = 1; for frequency register 0
    MSB |= 0x4000
    LSB |= 0x4000
    
    # Send LSB
    high, low = divmod(LSB, 0x100)
    spi.xfer([high, low])  # LSB
    
    # Send MSB
    high, low = divmod(MSB, 0x100)
    spi.xfer([high, low])  # MSB
    
    # Print the hexadecimal representation of MSB and LSB
    print(f"Frequency register MSB: {hex(MSB)}, LSB: {hex(LSB)}")
    
    # Phase register 0°
    spi.xfer([0xC0, 0x00])  # MSB
    print("Phase register 0xC000 \n")
    
    # Sine wave
    spi.xfer([0x00, 0x00])  # Sine
    print("Sine 0x0000 \n")
    
    channel = 7
    # Format the ADC readings as a string
    data = ""
    samples = 1024
    
    while samples > 0:
        r = adc1.ADCread(channel)
        reading = "{v}".format(v=r)
        data += reading + "\n"
        samples -= 1
    
    print(data)
    # Write the formatted data to a file on the Raspberry Pi
    write_data_to_file(data)        
    # Transfer the file to the Windows laptop
    transfer_file_to_laptop("/home/pedro/Desktop/log.txt")
    
    adc1.close()  # Close the SPI and cleanup GPIO

    
if __name__ == '__main__':
    main()
