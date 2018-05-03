from neopixel import *

LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

YELLOW_COLOR  = Color(255,255,0)
RED_COLOR     = Color(0,255,0)
GREEN_COLOR   = Color(255,0,0)
BLUE_COLOR    = Color(0,0,255)
MAGENTA_COLOR = Color(0,255,255)

RING            = 13
RING_CHANNEL    = 1
RING_COUNT      = 48
KNOB_INCREMENTS = 6

# ZIGZAG     = 19
ZIGZAG_MAX = 24

ring = Adafruit_NeoPixel(RING_COUNT, RING, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, RING_CHANNEL)
# zigzag = Adafruit_NeoPixel(RING_COUNT, ZIGZAG, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, RING_CHANNEL)

def ringWipe(ringColor, isOn, wait_ms=50):
    # print 'Ring: ', isOn, ' for ', ringColor.name, 'at ', ringColor.pos
    colorToUse = ringColor.color if isOn else Color(0, 0, 0)
    pos = (ringColor.knob / 6) - 1 + ringColor.startPos

    if isOn:
        start = ringColor.startPos
        end = pos
    else:
        start = pos
        end = ringColor.startPos + 24

    for i in range(start, end):
        ring.setPixelColor(pos, colorToUse)
    # Not yet showing zigzags
    # if pos == 0:
    #     zigzagWipe(ringColor.zigzag, isOn)

def zigzagWipe(zigzag, isOn, wait_ms=50):
    # print 'Zigzag: ', isOn , ' for ', zigzag.name, 'at ', zigzag.pos
    colorToUse = zigzag.color if isOn else Color(0, 0, 0)
    for i in range(zigzag.pos, zigzag.pos + ZIGZAG_MAX):
        ring.setPixelColor(i, colorToUse)

class Zigzag:
    def __init__(self, color, name, startPos):
        self.color = color
        self.name = name
        self.on = False
        self.pos = 0 + startPos

    def __str__(self):
        return self.name

    def setOn(self, isOn):
        self.on = isOn
        zigzagWipe(self, self.on)

yellowZigzag = Zigzag(YELLOW_COLOR, "YELLOW", 120)
redZigzag = Zigzag(RED_COLOR, "RED", 144)
greenZigzag = Zigzag(GREEN_COLOR, "GREEN", 168)
blueZigzag = Zigzag(BLUE_COLOR, "BLUE", 192)
magentaZigzag = Zigzag(MAGENTA_COLOR, "MAGENTA", 216)

class Ring:
    def __init__(self, color, name, startPos, zigzag):
        self.color = color
        self.name = name
        self.startPos = startPos
        self.knob = 0
        self.zigzag = zigzag

    def __str__(self):
        return self.name

    def knobForward(self):
        if self.knob >= 144:
            return
        # print 'Moving forward ', self.name, ' with knob ', self.knob
        self.knob += 1
        if self.knob % KNOB_INCREMENTS == 0:
            print 'Ring light ON with knob: ', self.knob
            ringWipe(self, True)
            ring.show()

    def knobBack(self):
        if self.knob <= 0:
            return
        # print 'Moving back ', self.name, ' with knob ', self.knob
        self.knob -= 1
        if self.knob % KNOB_INCREMENTS == 0:
            print 'Ring light OFF with knob: ', self.knob
            ringWipe(self, False)
            ring.show()


yellowRing = Ring(YELLOW_COLOR, "YELLOW", 0, yellowZigzag)
redRing = Ring(RED_COLOR, "RED", 24, redZigzag)
greenRing = Ring(GREEN_COLOR, "GREEN", 48, greenZigzag)
blueRing = Ring(BLUE_COLOR, "BLUE", 72, blueZigzag)
magentaRing = Ring(MAGENTA_COLOR, "MAGENTA", 96, magentaZigzag)
