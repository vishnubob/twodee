#!/usr/bin/env python

import math
import svgwrite
from svgwrite.mixins import Presentation

class StarMaker(object):
    def __init__(self, **params):
        self.margin = params.get("margin", 50)
        self.long_length = params.get("long_length", 200)
        self.short_length = params.get("short_length", 100)
        self.arm_count = params.get("arm_count", 5)
        self.angle_offset = params.get("angle_offset", math.pi)
        self.tab_width = params.get("tab_width", 20)

    def get_center(self):
        return (self.long_length + self.margin, self.long_length + self.margin)

    def get_angle(self, idx):
        angle_step = (math.pi * 2.0) / (self.arm_count * 2.0)
        return angle_step * idx + self.angle_offset

    def get_short_spoke(self, idx):
        angle = self.get_angle(idx)
        x = math.sin(angle) * self.short_length
        y = math.cos(angle) * self.short_length
        (x_center, y_center) = self.get_center()
        x += x_center
        y += y_center
        return (x, y)

    def get_long_spoke(self, idx):
        angle = self.get_angle(idx)
        x = math.sin(angle) * self.long_length
        y = math.cos(angle) * self.long_length
        (x_center, y_center) = self.get_center()
        x += x_center
        y += y_center
        return (x, y)

    def get_path(self):
        for idx in xrange(self.arm_count * 2 + 1):
            if (idx % 2):
                (x, y) = self.get_short_spoke(idx)
            else:
                (x, y) = self.get_long_spoke(idx)
            if idx == 0:
                cmd = 'M'
            else:
                cmd = 'L'
            yield str.join(' ', map(str, (cmd, x, y)))

    def get_spokes(self):
        for idx in xrange(self.arm_count * 2):
            if (idx % 2):
                spoke = self.get_short_spoke(idx)
            else:
                spoke = self.get_long_spoke(idx)
            coords = (self.get_center(), spoke)
            yield coords

    def get_tabs(self):
        offset = math.radians(30)
        offset1 = math.radians(120)
        for idx in xrange(self.arm_count):
            path = []
            # pt1
            spoke = self.get_long_spoke(idx * 2)
            path.append('M')
            path.extend(spoke)
            # pt2
            angle = self.get_angle(idx * 2)
            x = math.sin(angle + offset1) * self.tab_width + spoke[0]
            y = math.cos(angle + offset1) * self.tab_width + spoke[1]
            path.extend(('L', x, y))
            # pt3
            spoke = self.get_short_spoke(idx * 2 + 1)
            angle = self.get_angle(idx * 2 + 1)
            x = math.sin(angle - offset) * self.tab_width + spoke[0]
            y = math.cos(angle - offset) * self.tab_width + spoke[1]
            path.extend(('L', x, y))
            # pt4
            path.append('L')
            path.extend(spoke)
            # pt5
            x = math.sin(angle + offset) * self.tab_width + spoke[0]
            y = math.cos(angle + offset) * self.tab_width + spoke[1]
            path.extend(('L', x, y))
            # pt6
            spoke = self.get_long_spoke((idx + 1) * 2)
            angle = self.get_angle((idx + 1) * 2)
            x = math.sin(angle - offset1) * self.tab_width + spoke[0]
            y = math.cos(angle - offset1) * self.tab_width + spoke[1]
            path.extend(('L', x, y))
            # pt7
            path.append('L')
            path.extend(spoke)
            #
            path = str.join(' ', map(str, path))
            yield path
        
    def generate(self, svgfn="star.svg", profile="tiny"):
        dwg = svgwrite.Drawing(svgfn, profile=profile)
        # path
        star = dwg.g()
        path = dwg.path(self.get_path(), stroke="black", fill="white")
        star.add(path)
        dwg.add(star)
        # spokes
        spokes = dwg.g()
        for spoke in self.get_spokes():
            ln = dwg.line(*spoke, stroke="black")
            spokes.add(ln)
        dwg.add(spokes)
        # tabs
        tabs = dwg.g()
        for tab_path in self.get_tabs():
            tab_path = dwg.path(tab_path, stroke="black", fill="white")
            tabs.add(tab_path)
        dwg.add(tabs)
        #
        dwg.save()

if __name__ == "__main__":
    star = StarMaker()
    star.generate()
