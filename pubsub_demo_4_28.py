#!/usr/bin/env python3

#import encoder
import time
from neopixel import *
import argparse
from RPi import GPIO
from time import sleep

w, h = 32, 20;
matrix = [[0 for x in range(w)] for y in range(h)]
val = 0

for i in range(0,20):
        for j in range(0,32):
                matrix[i][j] =val
                val += 1
# yellow.row = 0
# yellow.col = 0

# red.row = 0
# red.col = 0

# green.row = 0
# green.col = 0

colMax = 32
rowMax = 4

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

#count = encoder.counter
count = 0
yellowCount = 0
redCount = 0
greenCount = 0
blueCount = 0
orangeCount = 0

clk1LastState = GPIO.input(clk1)
clk2LastState = GPIO.input(clk2)
clk3LastState = GPIO.input(clk3)
clk4LastState = GPIO.input(clk4)
clk5LastState = GPIO.input(clk5)

class LEDColor:
    def __init__(self, color, name):
        self.color = color
        self.name = name
        self.col = 0
        self.row = 0

    def __str__(self):
        return self.name

    def isLit(self):
        return self.row != 0 or self.col != 0

    def increment(self):
        if self.col < (colMax - 1):
            self.col += 1
        else:
            self.col = 0
            self.row += 1
        print self.color, ": ", self.row, self.col

    def decrement(self):
        if self.col == 0 and self.row == 0:
            return False

        if self.col == 0:
            self.col = colMax - 1
            self.row -= 1
            return True

        self.col -= 1
        return self.col == 0 and self.row == 0

yellow = LEDColor(Color(255,255,0), 'YELLOW')
red = LEDColor(Color(0,255,0), 'RED')
green = LEDColor(Color(255,0,0), 'GREEN')
blue = LEDColor(Color(0,0,255), 'BLUE')
orange = LEDColor(Color(165,255,0), 'ORANGE')
off = LEDColor(Color(0,0,0), 'OFF')

# LED MATRIX ANIMATIONS.

def redrawColor(ledColor, removeEnd, strip):
    if removeEnd:
        for col in range(0, colMax):
            strip.setPixelColor(matrix[ledColor.row + calculateOffset(ledColor) + 1][col], off.color)

    # Light up all full rows of color
    for row in range(0, ledColor.row):
        for col in range(0, colMax):
            drawColor(row, col, strip, ledColor)

    # Light up remaining lights in last row
    for col in range(0, ledColor.col):
        drawColor(ledColor.row, col, strip, ledColor)

    # Turn off the rest of lights in last row
    for col in range(ledColor.col, colMax):
        strip.setPixelColor(matrix[ledColor.row + calculateOffset(ledColor)][col], off.color)

def calculateOffset(ledColor):
    if ledColor == yellow:
        return 0

    offset = yellow.row + (1 if yellow.col > 0 else 0);

    if ledColor == red:
        # return total of yellow rows
        return offset

    offset += red.row + (1 if red.col > 0 else 0)

    if ledColor == green:
        # return total of yellow and red rows
        return offset

    offset += green.row + (1 if green.col > 0 else 0)

    if ledColor == blue:
        # return total of yellow, red, and green rows
        return offset

    offset += blue.row + (1 if blue.col > 0 else 0)

    # return total of yellow, red, green, and blue rows
    return offset

def drawColor(row, col, strip, ledColor, wait_ms=50):
    offset = calculateOffset(ledColor)
    strip.setPixelColor(matrix[row + offset][col], ledColor.color)
    if ledColor.col is 0:
        # Clear rest of the colors for this new row
        for i in range(1, colMax):
            strip.setPixelColor(matrix[row + offset][i], off.color)

def redrawColors(ledColor, removeEnd, strip):
    if ledColor == orange:
        return

    if ledColor == blue:
        if orange.isLit():
            redrawColor(orange, removeEnd, strip)

    if ledColor == green:
        if blue.isLit():
            redrawColor(blue, removeEnd, strip)
        if orange.isLit():
            redrawColor(orange, removeEnd, strip)

    if ledColor == red:
        if green.isLit():
            redrawColor(green, removeEnd, strip)
        if blue.isLit():
            redrawColor(blue, removeEnd, strip)
        if orange.isLit():
            redrawColor(orange, removeEnd, strip)

    if ledColor == yellow:
        if red.isLit():
            redrawColor(red, removeEnd, strip)
        if green.isLit():
            redrawColor(green, removeEnd, strip)
        if blue.isLit():
            redrawColor(blue, removeEnd, strip)
        if orange.isLit():
            redrawColor(orange, removeEnd, strip)

def add(ledColor, strip):
    print "adding ", ledColor, " at ", matrix[ledColor.row][ledColor.col]
    if ledColor.row > rowMax - 1:
        return
    drawColor(ledColor.row, ledColor.col, strip, ledColor)
    ledColor.increment()
    if (ledColor.col == 1):
        redrawColors(ledColor, False, strip)
    strip.show()


def remove(ledColor, strip):
    print 'remote ', ledColor, ' at ', matrix[ledColor.row][ledColor.col]
    if not ledColor.isLit():
        return
    removedRow = ledColor.decrement()

    offset = calculateOffset(ledColor)
    strip.setPixelColor(matrix[ledColor.row + offset][ledColor.col], off.color)

    if removedRow:
        print ledColor, ' row removed, redrawing...'
        redrawColors(ledColor, True, strip)
    strip.show()

#RING ANIMATIONS
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
    print count
    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')
        try:
            while True:
#                print ('Color wipe animations.')
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

#------YELLOW-----------------------------------------------------------------------------------------------
                if clk1State != clk1LastState:
                    if dt1State != clk1State:
                        remove(yellow, strip)
                    else:
                        add(yellow, strip)

#------------RED------------------------------------------------------------------------------------------
                if clk2State != clk2LastState:
                    if dt2State != clk2State:
                        remove(red, strip)
                    else:
                        add(red, strip)

#---------------GREEN--------------------------------------------------------------------------------------
                if clk3State != clk3LastState:
                    if dt3State != clk3State:
                        remove(green, strip)
                    else:
                        add(green, strip)

#---------------BLUE--------------------------------------------------------------------------------------
                if clk4State != clk4LastState:
                    if dt4State != clk4State:
                        remove(blue, strip)
                    else:
                        add(blue, strip)

#---------------ORANGE--------------------------------------------------------------------------------------
                if clk5State != clk5LastState:
                    if dt5State != clk5State:
                        remove(orange, strip)
                    else:
                        add(orange, strip)

                clk1LastState = clk1State
                clk2LastState = clk2State
                clk3LastState = clk3State
                clk4LastState = clk4State
                clk5LastState = clk5State
#                sleep(0.01)
        except KeyboardInterrupt:
            if args.clear:
                colorWipe(strip, Color(0,0,0), 10)

        finally:
            GPIO.cleanup()
