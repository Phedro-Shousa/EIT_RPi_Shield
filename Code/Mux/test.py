# SPI-Library
import spidev
# time-Library
import time
# GPIO-Library
import RPi.GPIO as GPIO
# ADG725-Library
import ADG725
# Keyboard Library for detecting key presses
import keyboard

# Setup GPIO
GPIO.setmode(GPIO.BCM)
Mux_1 = True
Mux_0 = False

def main():
    mux0 = ADG725.ADG725(Mux_0)
    mux1 = ADG725.ADG725(Mux_1)
    print("INIT \n")
    mux0.allOff()
    mux1.allOff()
    print("ALL OFF \n")

    i = 0
    j = 0
    print("Press the spacebar to switch channels for ChannelA.")
    print("Press Enter to switch channels for ChannelB.")

    while True:  # Infinite loop
        if keyboard.is_pressed('space'):
            # Set the channel A based on the current value of i
            mux0.setChannelA(i)
            mux1.setChannelA(i)
            print(f"ChannelA {i} \n")
            # Increment i, and reset to 0 when reaching 16
            i += 1
            if i == 15:
                i = 0
            time.sleep(0.2)  # Small delay to prevent rapid consecutive increments

        elif keyboard.is_pressed('enter'):
            # Set the channel B based on the current value of j
            mux0.setChannelB(j)
            mux1.setChannelB(j)
            print(f"ChannelB {j} \n")
            # Increment j, and reset to 0 when reaching 16
            j += 1
            if j == 15:
                j = 0
            time.sleep(0.2)  # Small delay to prevent rapid consecutive increments

if __name__ == '__main__':
    main()
