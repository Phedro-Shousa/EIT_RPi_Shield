import spidev
import RPi.GPIO as GPIO
import keyboard  # To detect keypresses

def main():
    freq = 10000000
    ClockFreq = 25000000
    
    print("Wav_Gem Test \n")
    GPIO.setmode(GPIO.BCM)
    spi = spidev.SpiDev(6, 2)
    spi.max_speed_hz = 1000000 
    spi.mode = 0b10

    while True:
        # Wait for an event
        event = keyboard.read_event()
        
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'up':
                freq += 100000
                print("Arrow up pressed: Increasing frequency to", freq)
            elif event.name == 'down':
                freq -= 100000
                print("Arrow down pressed: Decreasing frequency to", freq)
            elif event.name == 'right':
                freq *= 10
                print("Arrow right pressed: Multiplying frequency by 10 to", freq)
            elif event.name == 'left':
                freq //= 10
                print("Arrow left pressed: Dividing frequency by 10 to", freq)

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

    
if __name__ == '__main__':
    main()
