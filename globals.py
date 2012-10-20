#!/usr/bin/env python

import math
from decimal import Decimal

x = 0
y = 1

color_white = 255, 255, 255
color_black = 0, 0, 0

def calc_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Return decimal number as string, with 2 decimals
def twodec(dec):
    TWOPLACES = Decimal(10) ** -2
    return str(Decimal(dec).quantize(TWOPLACES))



