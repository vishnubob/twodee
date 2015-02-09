#!/usr/bin/env python

import math
import svgwrite
from svgwrite.mixins import Presentation

class Airplane(object):
    def __init__(self, height=8.5, width=11.0, scale=100):
        self.height = height * scale
        self.width = width * scale

    def get_origin(self):
        return (0, self.height / 2.0)

    def get_coord(self, step):
        angle = 90 - (11.25 * (step + 1))
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))
        if angle < 45 and angle > -45:
            print "X is constant"
            _y = self.height - self.width * (y / x) + (self.height / 2.0)
            coord = (self.width, _y)
        else:
            print "Y is constant"
            _x = self.height * (x / y)
            if (_x < 0):
                coord = (_x, self.height)
            else:
                coord = (_x, 0)
        print angle, (x, y), coord
        return coord

    def generate(self, svgfn="airplane.svg", profile="tiny"):
        dwg = svgwrite.Drawing(svgfn, profile=profile)
        origin = self.get_origin()
        print self.width, self.height
        print origin
        end = (self.width, origin[1])
        for x in range(5):
            point = self.get_coord(x)
            ln = dwg.line(origin, point, stroke="black")
            dwg.add(ln)
        dwg.save()

if __name__ == "__main__":
    star = Airplane()
    star.generate()

