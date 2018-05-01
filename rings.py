from neopixel import *
from main import LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT

RING            = 13
RING_CHANNEL    = 1
RING_COUNT      = 48
ZIGZAG          = 19
KNOB_INCREMENTS = 5

ring = Adafruit_NeoPixel(RING_COUNT, RING, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, RING_CHANNEL)
zigzag = Adafruit_NeoPixel(RING_COUNT, ZIGZAG, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, RING_CHANNEL)

def ringWipe(ledRing, isOn, wait_ms=50):
    print 'Ring: Adding', ledRing.name, 'at ', ledRing.pos
    colorToUse = ledRing.color if isOn else Color(0, 0, 0)
    ring.setPixelColor(ledRing.pos, colorToUse)
    ring.show()

class Ring:
    def __init__(self, color, name, startPos):
        self.color = color
        self.name = name
        self.pos = 0 + startPos
        self.knob = 0

    def __str__(self):
        return self.name

    def knobForward(self):
        print('Moving forward ', self.name, ' with pos ', self.pos)
        if self.knob >= 128:
            return
        self.knob += 1
        if self.knob % KNOB_INCREMENTS == 0:
            self.pos += 1
        ringWipe(self, True)

    def knobBack(self):
        print 'Moving back ', self.name, ' with pos ', self.pos
        ringWipe(self, False)
        if self.knob <= 0:
            return
        self.knob -= 1
        if self.knob % KNOB_INCREMENTS == 0:
            self.pos -= 1


yellowRing = Ring(Color(255,255,0), "YELLOW", 0)
redRing = Ring(Color(0,255,0), "RED", 24)
greenRing = Ring(Color(255,0,0), "GREEN", 48)
blueRing = Ring(Color(0,0,255), "BLUE", 72)
magentaRing = Ring(Color(0,255,255), "MAGENTA", 96)
