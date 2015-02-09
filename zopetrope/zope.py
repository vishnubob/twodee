#!/usr/bin/env python

import math
import svgwrite
from svgwrite import inch, cm, mm
from svgwrite.mixins import Presentation
from svgwrite import shapes

class Zopetrope(object):
    ObjectMap = ["padding", "slit", "padding", "frame"]

    def __init__(self):
        # default units are in inches
        self.paper_height = 12 * inch
        self.paper_width = 12 * inch
        # frames
        self.frame_count = 8
        self.frame_width = 1
        self.frame_height = 1
        # slits
        self.slit_width = .1
        self.slit_height = 1
        # strip
        self.strip_width = 11
        self.strip_height = 1.5
        # margin
        self.x_margin = .1
        self.y_margin = .1

    @property
    def padding(self):
        used_space = self.strip_width - (self.slit_width * (self.frame_count + 1) + self.frame_width * self.frame_count)
        return used_space / (2 * (self.frame_count + 1))
    
    def get_strip_origin(self):
        return (self.x_margin, self.y_margin)

    def get_object_name(self, index):
        return self.ObjectMap[index % len(self.ObjectMap)]

    def get_xoffset(self, index):
        offsets = {
            "padding": self.padding,
            "slit": self.slit_width,
            "frame": self.frame_width
        }
        xoffset = sum([offsets[self.get_object_name(x)] for x in range(index)]) + self.x_margin
        return xoffset

    def get_object_size(self, index):
        objname = self.get_object_name(index)
        if objname == "padding":
            return (self.padding, self.strip_height)
        if objname == "slit":
            return (self.slit_width, self.slit_height)
        if objname == "frame":
            return (self.frame_width, self.frame_height)

    def get_object_origin(self, index):
        xoffset = self.get_xoffset(index)
        sz = self.get_object_size(index)
        yoffset = (self.strip_height - sz[1]) / 2.0 + self.y_margin
        return (xoffset, yoffset)

    def unitize(self, xy):
        return (xy[0] * inch, xy[1] * inch)

    def build_strip(self):
        origin = self.unitize(self.get_strip_origin())
        size = (self.strip_width * inch, self.strip_height * inch)
        rct = shapes.Rect(origin, size, stroke="black", stroke_width=1, fill="white")
        self.canvas.add(rct)
        for index in range(self.frame_count * 4 + 2):
            objname = self.get_object_name(index)
            if objname in ("padding", "frame"):
                continue
            size = self.unitize(self.get_object_size(index))
            origin = self.unitize(self.get_object_origin(index))
            print objname, size, origin
            rct = shapes.Rect(origin, size, stroke="black", stroke_width=1, fill="white")
            self.canvas.add(rct)

    def build_circle(self):
        circumfrence = self.strip_width - (self.padding * 2) - self.slit_width
        radius = circumfrence / (2 * math.pi)
        center = (radius + self.x_margin, radius + self.y_margin * 2 + self.strip_height)
        center = self.unitize(center)
        cir = shapes.Circle(center=center, r=radius * inch, stroke="black", stroke_width=1, fill="white")
        self.canvas.add(cir)
        cir = shapes.Circle(center=center, r=.185 * inch, stroke="black", stroke_width=1, fill="white")
        self.canvas.add(cir)

    def generate(self, svgfn="zopetrope.svg", profile="tiny"):
        svgfn = "zopetrope.svg"
        self.canvas = svgwrite.Drawing(svgfn, profile=profile)
        self.build_strip()
        self.build_circle()
        self.canvas.save()

if __name__ == "__main__":
    zope = Zopetrope()
    zope.generate()
