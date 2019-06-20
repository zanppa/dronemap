# circle2.py
# 
# Reads airport runway data from json file "lentokentat.json"
# and generates a zone that is a given radius away from the runway edges.
# Zones are then printed out as json.
#
# This script is used to generate no-drone-zones around runways.
# In Finland it is forbidden to fly drones closer than 5 km to 
# runway edges, and this tool can be used to approximately genereate the
# restriction zones to be drawn on a map.
#
# Copyright (C) 2018 Lauri Peltonen

# References:
# https://gis.stackexchange.com/questions/268250/generating-polygon-representing-rough-100km-circle-around-latitude-longitude-poi/268277
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
# https://stackoverflow.com/questions/40385782/make-a-union-of-polygons-in-python-geopandas-or-shapely-into-a-single-geometr

import json

import numpy as np
import json
import geog
import shapely.geometry
from shapely.ops import cascaded_union

CIRCLE_RADIUS = 5000   # 5 km clearance from runways
CIRCLE_PARTS = 125     # 125 segments at 5 km radius is about 250 m segment length
RUNWAY_PART_LENGTH = 250	# Runways are segmented to 250 m parts

# This is used to interpolate between runway ends
def getEquidistantPoints(p1, p2, parts):
    return zip(np.linspace(p1[0], p2[0], parts+1), np.linspace(p1[1], p2[1], parts+1))

# Read the source json file
with open('lentokentat.json') as json_file:
  data = json.load(json_file)
  
  features = []
  # Loop through all airports (array of dictionaries)
  for airport in data['airports']:
    id = airport['id']
    name = airport['name']
    date = airport['date']
    updated = airport['updated']
    # center = airport['center']  # Not used at the moment

    # Loop through the runways
    polygons = []
    for runway, rwdata in airport['runways'].items():
      # Runway endpoints
      end1 = rwdata['end1']
      end2 = rwdata['end2']
      length = rwdata['length']  # Runway length in meters
      width = rwdata['width']

      parts = length // RUNWAY_PART_LENGTH
      points = getEquidistantPoints(end1, end2, parts)

      for point in points:
        p = shapely.geometry.Point(point)
        r = CIRCLE_RADIUS + width/2
        angles = np.linspace(0, 360, CIRCLE_PARTS)
        polygon = geog.propagate(p, angles, r)
        p = shapely.geometry.Polygon(polygon)
        polygons.append(p)

    # Combine all runways and their parts
    shape = cascaded_union(polygons)
    geometry = shapely.geometry.mapping(shape)

    airportdata = {"type":"Feature","id":id,"properties":{"name":name,"type":"R"},"geometry":geometry,"publ":date,"updated":updated}
    features.append(airportdata)

  final = {"type":"FeatureCollection", "features":features}
  print json.dumps(final)
