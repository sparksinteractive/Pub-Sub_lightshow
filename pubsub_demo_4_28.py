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
yRow = 0
yCol = 0

rRow = 0
rCol = 0

gRow = 0
gCol = 0

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

    def __str__(self):
        return self.name

yellow = LEDColor(Color(255,255,0), 'YELLOW')
red = LEDColor(Color(0,255,0), 'RED')
green = LEDColor(Color(255,0,0), 'GREEN')
blue = LEDColor(Color(0,0,255), 'BLUE')
orange = LEDColor(Color(165,255,0), 'ORANGE')
off = LEDColor(Color(0,0,0), 'OFF')

# LED MATRIX ANIMATIONS.

def hasRed():
    return rRow != 0 or rCol != 0

def hasGreen():
    return gRow != 0 or gCol != 0

def redrawRed():
    for row in range(0,rRow):
        for col in range(0,colMax):
            drawColor(row, col, strip, red)
    for col in range(0,rCol):
        drawColor(rRow, col, strip, red)

def redrawGreen():
    for row in range(0, gRow):
        for col in range(0, colMax):
            drawColor(row, col, strip, green)
    for col in range(0, gCol):
        drawColor(gRow, col, strip, green)

def calculateOffset(ledColor):
    switcher = {
        yellow: 0,
        red: yRow + (1 if yCol > 0 else 0),
        green: rRow + yRow + (1 if yCol > 0 else 0) + (1 if rCol > 0 else 0),
    }
    return switcher.get(ledColor)

def drawColor(row, col, strip, ledColor, wait_ms=50):
    offset = calculateOffset(ledColor)
    strip.setPixelColor(matrix[row + offset][col], ledColor.color)
    if col == 0:
        # Clear rest of the colors for this new row
        for i in range(1, colMax):
            strip.setPixelColor(matrix[row + offset][i], off.color)

def incrementYellow():
    global yRow, yCol
    if yCol < (colMax - 1):
        yCol += 1
    else:
        yCol = 0
        yRow += 1
    print yellow, ": ", yRow, yCol

def incrementGreen():
    global gRow, gCol
    if gCol < (colMax - 1):
        gCol += 1
    else:
        gCol = 0
        gRow += 1
    print green, ": ", gRow, gCol

def incrementRed():
    global rRow, rCol
    if rCol < (colMax - 1):
        rCol += 1
    else:
        rCol = 0
        rRow += 1
    print red, ": ", rRow, rCol

def incrementColor(ledColor):
    switcher = {
        yellow: incrementYellow,
        red: incrementRed,
        green: incrementGreen
    }
    return switcher.get(ledColor)()

def decrementGreen():
    global gRow, gCol
    if gCol == 0:
        gCol = colMax - 1
        gRow -= 1
    else:
        gCol -= 1

def redrawColors(ledColor):
    switcher = {
        yellow: yCol,
        red: rCol,
        green: gCol
    }
    col = switcher.get(ledColor)

    if (col != 1):
        return

    if ledColor == green:
        return
    if hasGreen():
        redrawGreen()

    if ledColor == red:
        return
    if hasRed():
        redrawRed()


#------ADDING COLORS-----------------------------------------------------------------------------------------------


def add(ledColor, row, col, strip):
    print "adding ", ledColor, " at ", matrix[row][col]
    if row > rowMax - 1:
        return
    drawColor(row, col, strip, ledColor)
    incrementColor(ledColor)
    redrawColors(ledColor)
    strip.show()


#------ADDING COLORS-----------------------------------------------------------------------------------------------


def removeYellow(strip, color, wait_ms=50):
    global yRow, yCol
    print 'remove yellow at: ', matrix[yRow][yCol]

    removedRow = False
    if yRow <= 0 and yCol <= 0:
        return
    else:
        if yCol == 0:
            yCol = colMax - 1
            yRow -= 1
            removedRow = True
        else:
            yCol -= 1
            removedRow = yCol == 0 and yRow == 0
        strip.setPixelColor(matrix[yRow][yCol], color)

    if removedRow and (rCol != 0 or rRow != 0):
        for col in range(0,colMax):
            drawColor(rRow + 1, col, strip, off)
        redrawRed()
    strip.show()

def removeRed(strip, color, wait_ms=50):
    global rRow, rCol
    print 'remove red at: ', matrix[rRow][rCol]

    removedRow = False
    if rRow <= 0 and rCol <= 0:
        return
    if rCol == 0:
        rCol = colMax -1
        rRow -= 1
        removedRow = True
    else:
        rCol -= 1
        removedRow = rCol == 0 and rRow == 0

    if removedRow and hasGreen():
        for col in range(0,colMax):
            drawColor(gRow + 1, col, strip, off)
        redrawGreen()

    rRowRemove = rRow + yRow
    if (yCol > 0):
        rRowRemove += 1
    strip.setPixelColor(matrix[rRowRemove][rCol], color)
    strip.show()

def removeGreen(strip, color, wait_ms=50):
    global gRow, gCol
    print 'remove green at: ', matrix[gRow][gCol]
    if gRow <= 0 and gCol <= 0:
        return
    decrementGreen()
    rowToRemove = gRow + rRow + yRow
    if rCol > 0:
        rowToRemove += 1
    if yCol > 0:
        rowToRemove += 1
    strip.setPixelColor(matrix[rowToRemove][gCol], color)
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
                        removeYellow(strip, Color(0,0,0))
                    else:
                        add(yellow, yRow, yCol, strip)

#------------RED------------------------------------------------------------------------------------------
                if clk2State != clk2LastState:
                    if dt2State != clk2State:
                        removeRed(strip, Color(0, 0, 0))
                    else:
                        add(red, rRow, rCol, strip)
#---------------GREEN--------------------------------------------------------------------------------------
                if clk3State != clk3LastState:
                    if dt3State != clk3State:
                        removeGreen(strip, Color(0, 0, 0))
                    else:
                        add(green, gRow, gCol, strip)

                if clk4State != clk4LastState:
                    if dt4State != clk4State:
                        colorWipe(strip, Color(0, 0, 0), 'off')
                        count -= 1
                    else:
                        colorWipe(strip, Color(140, 255, 0), 'orange')
                        count += 1

                if clk5State != clk5LastState :
                    if dt5State != clk5State:
                        colorWipe(strip, Color(0, 0, 0), 'off')
                        count -= 1

                    if dt5State == clk5State:
                        colorWipe(strip, Color(255, 255, 0), 'yellow')
                        count += 1

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
