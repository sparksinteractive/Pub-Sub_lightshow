#!/usr/bin/env python3

#import encoder
import time
from neopixel import *
import argparse
from RPi import GPIO
from time import sleep
from led_colors import *

# encoder config
clk1 = 17
dt1 = 27

clk2 = 5
dt2 = 6

clk3 = 13
dt3 = 25

clk4 = 26
dt4 = 21

clk5 = 20
dt5 = 16

ring1 = 0
ring2 = 24

# LED strip configuration:
LED_COUNT    = 300      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
RING_COUNT     = 48
RING          = 19

#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS    = 20     # Set to 0 for darkest and 255 for brightest
LED_INVERT    = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
RING_CHANNEL    = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clk2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clk3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clk4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clk5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

clk1LastState = GPIO.input(clk1)
clk2LastState = GPIO.input(clk2)
clk3LastState = GPIO.input(clk3)
clk4LastState = GPIO.input(clk4)
clk5LastState = GPIO.input(clk5)

# RING ANIMATIONS
def ringWipe(strip, color, ringNumber, shade, wait_ms=50):
    print 'Ring: Adding', shade, 'at ', ring1
    ring.setPixelColor(ringNumber, color)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    ring = Adafruit_NeoPixel(RING_COUNT, RING, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, RING_CHANNEL)

    # Intialize the library (must be called once before other functions).
    strip.begin()
    ring.begin()
    print ('Press Ctrl-C to quit.')

    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
        try:
            while True:
                clk1State = GPIO.input(clk1)
                dt1State = GPIO.input(dt1)
                clk2State = GPIO.input(clk2)
                dt2State = GPIO.input(dt2)
                clk3State = GPIO.input(clk3)
                dt3State = GPIO.input(dt3)
                clk4State = GPIO.input(clk4)
                dt4State = GPIO.input(dt4)
                clk5State = GPIO.input(clk5)
                dt5State = GPIO.input(dt5)

#-----------YELLOW-----------------------------------------------------------------------------------------------
                if clk1State != clk1LastState:
                    if dt1State != clk1State:
                        remove(yellow, strip)
                    else:
                        add(yellow, strip)

#-----------RED--------------------------------------------------------------------------------------------------
                if clk2State != clk2LastState:
                    if dt2State != clk2State:
                        remove(red, strip)
                    else:
                        add(red, strip)

#-----------GREEN------------------------------------------------------------------------------------------------
                if clk3State != clk3LastState:
                    if dt3State != clk3State:
                        remove(green, strip)
                    else:
                        add(green, strip)

#-----------BLUE-------------------------------------------------------------------------------------------------
                if clk4State != clk4LastState:
                    if dt4State != clk4State:
                        remove(blue, strip)
                    else:
                        add(blue, strip)

#-----------MAGENTA----------------------------------------------------------------------------------------------
                if clk5State != clk5LastState:
                    if dt5State != clk5State:
                        remove(magenta, strip)
                    else:
                        add(magenta, strip)

                clk1LastState = clk1State
                clk2LastState = clk2State
                clk3LastState = clk3State
                clk4LastState = clk4State
                clk5LastState = clk5State
        except KeyboardInterrupt:
            if args.clear:
                colorWipe(strip, Color(0,0,0), 10)

        finally:
            GPIO.cleanup()
