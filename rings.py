import math
from neopixel import *
from main import LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT

YELLOW_COLOR  = Color(255,255,0)
RED_COLOR     = Color(0,255,0)
GREEN_COLOR   = Color(255,0,0)
BLUE_COLOR    = Color(0,0,255)
MAGENTA_COLOR = Color(0,255,255)

RING            = 13
RING_CHANNEL    = 1
RING_COUNT      = 240
KNOB_INCREMENTS = 6
RING_BRIGHTNESS = 50

KNOB_MAX = 144
RING_SIZE = 24

start = 1

# ZIGZAG     = 19

ring = Adafruit_NeoPixel(RING_COUNT, RING, LED_FREQ_HZ, LED_DMA, LED_INVERT, RING_BRIGHTNESS, RING_CHANNEL)

def ringWipe(ringColor, isOn, wait_ms=50):
    colorToUse = ringColor.color if isOn else Color(0, 0, 0)
    if isOn:
        #turn on the lights
        colorToUse = ringColor.color
        for i in range(ringColor.startPos, ringColor.pos):
            ring.setPixelColor(i, colorToUse)
            if ringColor.pos > ringColor.startPos:
                zigzagWipe(ringColor.zigzag, isOn)
    else:
        #turn off the lights
        for i in range(ringColor.startPos + 23, ringColor.pos, -1):
            ring.setPixelColor(i, Color(0,0,0))
            if ringColor.pos < ringColor.startPos:
                zigzagWipe(ringColor.zigzag, isOn)

def zigzagWipe(zigzag, isOn, wait_ms=50):
#    print 'Zigzag: ', 'turning ON ' if isOn else 'turning OFF ', ' for ', zigzag.name, 'at ', zigzag.pos
    colorToUse = zigzag.color if isOn else Color(0, 0, 0)
    for i in range(zigzag.pos, zigzag.pos + zigzag.length):
        ring.setPixelColor(i, colorToUse)

class Zigzag:
    def __init__(self, color, name, startPos, length):
        self.color = color
        self.name = name
        self.on = False
        self.pos = 0 + startPos
        self.startPos = startPos
        self.length = length

    def __str__(self):
        return self.name

    def setOn(self, isOn):
        self.on = isOn
        zigzagWipe(self, self.on)

yellowZigzag = Zigzag(YELLOW_COLOR, "YELLOW", 120, 22)
redZigzag = Zigzag(RED_COLOR, "RED", 144, 14)
greenZigzag = Zigzag(GREEN_COLOR, "GREEN", 160, 8)
blueZigzag = Zigzag(BLUE_COLOR, "BLUE", 170, 14)
magentaZigzag = Zigzag(MAGENTA_COLOR, "MAGENTA", 186, 22)

class Ring:
    def __init__(self, color, name, startPos, zigzag):
        self.color = color
        self.name = name
        self.pos = 0 + startPos
        self.startPos = startPos
        self.knob = 0
        self.zigzag = zigzag

    def __str__(self):
        return self.name

    def knobForward(self):
        if self.knob >= KNOB_MAX or self.pos >= RING_SIZE + self.startPos:
            return
        self.knob += 1
        self.pos = (self.knob / 6)
        self.pos = int(math.floor(self.pos)) + self.startPos;
        ringWipe(self, True)
        ring.show()

    def knobBack(self):
        if self.knob <= 0 or self.pos < 0 + self.startPos:
            return
        # print 'Moving back ', self.name, ' with pos ', self.pos, ' and knob ', self.knob
        self.knob -= 1
        self.pos = (self.knob / 6)
        self.pos = int(math.floor(self.pos)) + self.startPos;
        ringWipe(self, False)
        ring.show()

yellowRing = Ring(YELLOW_COLOR, "YELLOW", 0, yellowZigzag)
redRing = Ring(RED_COLOR, "RED", 24, redZigzag)
greenRing = Ring(GREEN_COLOR, "GREEN", 48, greenZigzag)
blueRing = Ring(BLUE_COLOR, "BLUE", 72, blueZigzag)
magentaRing = Ring(MAGENTA_COLOR, "MAGENTA", 96, magentaZigzag)
