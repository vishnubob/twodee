#!/usr/bin/env python

import math
import svgwrite
from svgwrite.mixins import Presentation
from svgwrite.shapes import *

def inch(x):
    return x * 90

def fingers(count, width, depth, positive=True, origin=(0, 0), func=lambda x: x):
    offset = 0
    cursor = origin
    if not positive:
        offset = 2
        cursor = (cursor[0], cursor[1])
    path = [map(func, cursor)]
    for fidx in range(count * 2 - 1):
        step = (fidx + offset) % 4
        if step in (0, 2):
            cursor = (cursor[0] + width, cursor[1])
        elif step == 1:
            cursor = (cursor[0], cursor[1] + depth)
        elif step == 3:
            cursor = (cursor[0], cursor[1] - depth)
        path.append(map(func, cursor))
    print path
    return path

def finger_path(*args, **kw):
    path = fingers(*args, **kw)
    _path = ['M'] + path[0]
    for coords in path[1:]:
        _path.extend(['L'] + coords)
    #_path.extend(('L', 0, 0))
    path = str.join(' ', map(str, _path))
    return path

class ShroudMaker(object):
    def generate_top(self, svgfn="shroud_top.svg", profile="full"):
        dwg = svgwrite.Drawing(svgfn, profile=profile, size=(inch(20), inch(20)))
        left_corner = "translate(%s,%s)" % (inch(10), inch(10))
        top = dwg.g(transform=left_corner)
        print finger_path(6, .5, .5, func=inch)
        path = dwg.path(finger_path(7, 3.0 / 7, 3/8.0, func=inch, positive=True), stroke="black", fill="white")
        top.add(path)
        dwg.add(top)
        dwg.save()

    def generate_endcap(self, svgfn="shroud_endcap.svg", profile="full"):
        dwg = svgwrite.Drawing(svgfn, profile=profile, size=(inch(20), inch(20)))
        # path
        #top = Line((0, 0), (inch(3), 0), stroke='black')
        print
        top = dwg.path(finger_path(7, 3.0 / 7, 3/8.0, func=inch, positive=True), stroke="black", fill="white")
        print
        rot1 = "rotate(20, %s, %s)" % (inch(3), 0)
        #side1 = Line((inch(3), 0), (inch(3), inch(7)), stroke='black', transform=rot1)
        side1 = dwg.path(finger_path(5, 6.0 / 5, 3/8.0, func=inch, origin=(3, 0), positive=True), stroke="black", fill="white", transform=rot1)
        rot2 = "rotate(160, %s, %s)" % (inch(0), 0)
        #side2 = Line((inch(0), 0), (inch(0), inch(7)), stroke='black', transform=rot2)
        side2 = dwg.path(finger_path(5, 6.0 / 5, 3/8.0, func=inch, positive=False), stroke="black", fill="white", transform=rot2)
        left_corner = "translate(%s,%s)" % (inch(10), inch(10))
        endcap = dwg.g(transform=left_corner)
        # bottom
        y = abs(math.sin(math.radians(180 + 20)) * 7)
        x1 = math.cos(math.radians(180 + 20)) * 7
        x2 = math.cos(math.radians(-20)) * 7 + 3
        print x1, x2, y, abs(x1) + abs(x2)
        bottom = Line((inch(x1), inch(y)), (inch(x2), inch(y)), stroke='black')
        endcap.add(top)
        endcap.add(side1)
        endcap.add(side2)
        endcap.add(bottom)
        dwg.add(endcap)
        dwg.save()

if __name__ == "__main__":
    shroud = ShroudMaker()
    shroud.generate_endcap()
    shroud.generate_top()
