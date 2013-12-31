#!/usr/bin/env python

import math
import svgwrite
from svgwrite.mixins import Presentation

class Airplane(object):
    def __init__(self, height=8.5, width=11.0, dpi=72):
        self.dpi = dpi
        self.height = height * self.dpi
        self.width = width * self.dpi

    def get_origin(self):
        return (0, self.height / 2.0)

    def get_coord(self, step):
        angle = 90 - (11.25 * (step + 1))
        if angle == 0:
            return (self.width, self.height / 2.0)
        if angle < 0:
            angle += 360
        slope = math.tan(math.radians(angle))
        _y = (slope * self.width) + (self.height / 2.0)
        _x = (1 / slope) * (self.height / 2.0)
        _x = abs(_x)
        if _x < self.width:
            if (_y > 0):
                return (_x, 0)
            else:
                return (_x, self.height)
        else:
            return (self.width, _y)

    def generate(self, svgfn="airplane.svg", profile="tiny"):
        inch_width = "%.2fin" % (self.width / self.dpi)
        inch_height = "%.2fin" % (self.height / self.dpi)
        dwg = svgwrite.Drawing(svgfn, size=(inch_width, inch_height), profile=profile)
        origin = self.get_origin()
        end = (self.width, origin[1])
        #ln = dwg.line((self.width, 0), (self.width, self.height), stroke="black")
        #dwg.add(ln)
        for x in range(15):
            point = self.get_coord(x)
            ln = dwg.line(origin, point, stroke="black")
            dwg.add(ln)
        dwg.save()

if __name__ == "__main__":
    airplane = Airplane(12, 12)
    airplane.generate()
