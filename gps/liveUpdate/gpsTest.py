import random
import time

latDeg = 34
lonDeg = -118
alt = 1000

coor = open('coordinates.txt', 'w+')
coor.write("")

i = -5

while True:
    latMin = float(4) + float(i/10)
    lonMin = float(26)
    lat = (latDeg+(latMin/60))
    lon = (lonDeg-(lonMin/60))
    newCoor = ( 
            '%s,%s,%s'
      	) %(lon, lat, alt)

    with open('coordinates.txt', 'a+') as coor: 
        print newCoor
        coor.write(newCoor + '\n')

    with open("position.kml", "w") as pos:
        kmlHead = (
            """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Paths</name>
    <description>Examples of paths. Note that the tessellate tag is by default
      set to 0. If you want to create tessellated lines, they must be authored
      (or edited) directly in KML.</description>
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>4</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff00</color>
      </PolyStyle>
    </Style>
    <Placemark>
      <name>Absolute Extruded</name>
      <description>Transparent green wall with yellow outlines</description>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>\n""" 
            )
        kmlFoot = (
            """</coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>\n"""
            )
        coor = open('coordinates.txt', 'r')

        pos.write(kmlHead + coor.read() + kmlFoot)
    print i
    i += 1
    time.sleep(1)