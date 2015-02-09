#!/usr/bin/env python

from flask import Flask, make_response
import json
import math

app = Flask(__name__)

def build_svg(nodes):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" height="500" width="500">%s</svg>\n'
    out = []
    for (name, attrs) in nodes:
        attrs = ['%s="%s"' % attr for attr in attrs.items()]
        attrs = str.join(" ", attrs)
        node = "<%s %s />" % (name, attrs)
        out.append(node)
    out = str.join('\n', out)
    return svg % out


class Node(object):
    Name = "__node__"

    def __init__(self, **kw):
        self.kw = kw

    def node(self):
        return (self.Name, self.kw)

class Circle(Node):
    Name = "circle"

class Arab(object):
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy

    def render(self):
        r = self.cy / 2.0
        cc = Circle(cx=self.cx, cy=self.cy, r=r, fill="none", stroke="black", linewidth="1")
        nodes = [cc.node()]
        count = 12
        deg = 360.0 / count
        for idx in range(count):
            x = r * math.cos(math.radians(deg * idx)) + self.cx
            y = r * math.sin(math.radians(deg * idx)) + self.cy
            c = Circle(cx=x, cy=y, r=r, fill="none", stroke="black", linewidth="1")
            nodes.append(c.node())
        return build_svg(nodes)

@app.route('/')
def hello_world():
    f = open("draw.html")
    html = f.read()
    return html

@app.route('/draw.svg')
def draw_svg():
    arab = Arab(300, 300)
    svg = arab.render()
    response = make_response(svg)
    response.content_type = 'image/svg+xml'
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
