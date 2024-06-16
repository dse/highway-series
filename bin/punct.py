#!/usr/bin/env fontforge
# -*- mode: python; coding: utf-8 -*-

import fontforge
import json
import os

metricsData = json.loads(open("data/chars.json", "r").read())
metricsByChar = metricsData["chars"]
seriesIdxMap = metricsData["seriesIdxMap"]
metricsCapHeightBasis = metricsData["capHeightBasis"]

def main():
    setPunctMetrics("src/series-a.sfd", "Series A")
    setPunctMetrics("src/series-b.sfd", "Series B")

def setPunctMetrics(filename, seriesName):
    seriesIdx = seriesIdxMap[seriesName]
    print(seriesIdx)
    font = fontforge.open(filename)
    font.layers.add("defh", True, True)
    for char in metricsByChar:
        metrics = metricsByChar[char]
        codepoint = ord(char)
        glyph = font.createChar(codepoint)
        factor = font.capHeight / metricsCapHeightBasis
        lsb = metrics["lsb"]
        rsb = metrics["rsb"]
        width = metrics["width"]
        print("%s: lsb = %s; width = %s; rsb = %s" % (repr(char), repr(lsb), repr(width), repr(rsb)))
        if type(lsb) is list:
            lsb = 0 if len(lsb) <= seriesIdx else lsb[seriesIdx]
        if type(rsb) is list:
            rsb = 0 if len(rsb) <= seriesIdx else rsb[seriesIdx]
        if type(width) is list:
            width = 0 if len(width) <= seriesIdx else width[seriesIdx]
        print("%s: lsb = %s; width = %s; rsb = %s" % (repr(char), repr(lsb), repr(width), repr(rsb)))
        lsb = int(round(lsb * factor))
        rsb = int(round(rsb * factor))
        width = int(round(width * factor))
        print("%s: lsb = %s; width = %s; rsb = %s" % (repr(char), repr(lsb), repr(width), repr(rsb)))
        glyph.left_side_bearing = lsb
        glyph.right_side_bearing = rsb
        glyph.width = width + lsb + rsb
        layer = glyph.layers["defh"]
        if lsb != 0 or rsb != 0:
            glyph.activeLayer = 'defh'
            pen = glyph.glyphPen()
            if lsb != 0:
                pen.moveTo((lsb, 0))
                pen.lineTo((lsb, font.capHeight))
                pen.closePath()
            if rsb != 0:
                pen.moveTo((width + lsb, 0))
                pen.lineTo((width + lsb, font.capHeight))
                pen.closePath()
            glyph.draw(pen)
    if os.path.splitext(filename)[1] == ".sfd":
        font.save(filename)
    else:
        font.generate(filename)

main()