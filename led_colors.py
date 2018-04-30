from neopixel import *

w, h = 32, 20;
matrix = [[0 for x in range(w)] for y in range(h)]
val = 0

for i in range(0,20):
    for j in range(0,32):
        matrix[i][j] =val
        val += 1

colMax = 32
rowMax = 4

class LEDColor:
    def __init__(self, color, name, id):
        self.color = color
        self.name = name
        self.col = 0
        self.row = 0
        self.id = id

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

    def getPosition(self):
        return matrix[self.row][self.col]

yellow = LEDColor(Color(255,255,0), 'YELLOW', 0)
red = LEDColor(Color(0,255,0), 'RED', 1)
green = LEDColor(Color(255,0,0), 'GREEN', 2)
blue = LEDColor(Color(0,0,255), 'BLUE', 3)
magenta = LEDColor(Color(0,255,255), 'MAGENTA', 4)
off = LEDColor(Color(0,0,0), 'OFF', -999999)

def redrawColor(ledColor, removeEnd, strip):
    if removeEnd:
        for col in range(0, colMax):
            strip.setPixelColor(matrix[ledColor.row + calculateOffset(ledColor) + 1][col], off.color)

    # Light up all full rows of color
    for row in range(0, ledColor.row):
        for col in range(0, colMax):
            drawColor(row, col, strip, ledColor, False)

    # Light up remaining lights in last row
    for col in range(0, ledColor.col):
        drawColor(ledColor.row, col, strip, ledColor, False)

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

def drawColor(row, col, strip, ledColor, clear = True, wait_ms=50):
    print 'Redrawing ', ledColor
    offset = calculateOffset(ledColor)
    strip.setPixelColor(matrix[row + offset][col], ledColor.color)
    if ledColor.col is 0 and clear:
        # Clear rest of the colors for this new row
        for i in range(1, colMax):
            strip.setPixelColor(matrix[row + offset][i], off.color)

def redrawColors(ledColor, removeEnd, strip):
    if ledColor == magenta:
        return

    if ledColor == blue:
        if magenta.isLit():
            redrawColor(magenta, removeEnd, strip)

    if ledColor == green:
        if blue.isLit():
            redrawColor(blue, removeEnd, strip)
        if magenta.isLit():
            redrawColor(magenta, removeEnd, strip)

    if ledColor == red:
        if green.isLit():
            redrawColor(green, removeEnd, strip)
        if blue.isLit():
            redrawColor(blue, removeEnd, strip)
        if magenta.isLit():
            redrawColor(magenta, removeEnd, strip)

    if ledColor == yellow:
        if red.isLit():
            redrawColor(red, removeEnd, strip)
        if green.isLit():
            redrawColor(green, removeEnd, strip)
        if blue.isLit():
            redrawColor(blue, removeEnd, strip)
        if magenta.isLit():
            redrawColor(magenta, removeEnd, strip)

#
# Adds a color to the LED strip. Returns resulting data about this color as a dictionary
#
def add(ledColor, strip):
    print "adding ", ledColor, " at ", matrix[ledColor.row][ledColor.col]
    if ledColor.row > rowMax - 1:
        return
    drawColor(ledColor.row, ledColor.col, strip, ledColor)
    ledColor.increment()
    if (ledColor.col == 1):
        redrawColors(ledColor, False, strip)
    strip.show()

#
# Removes a color from the LED strip. Returns resulting data about this color as a dictionary
#
def remove(ledColor, strip):
    print 'remove ', ledColor, ' at ', matrix[ledColor.row][ledColor.col]
    if not ledColor.isLit():
        return
    removedRow = ledColor.decrement()

    offset = calculateOffset(ledColor)
    strip.setPixelColor(matrix[ledColor.row + offset][ledColor.col], off.color)

    if removedRow:
        print ledColor, ' row removed, redrawing...'
        redrawColors(ledColor, True, strip)
    strip.show()
