# A tool to automatically rewind geojson poplygons 
# to follow right-hand rule
# Copyright (C) 2019 Lauri Peltonen

import sys
import json
import geojson_rewind


# Read input data from stdin until EOF
data = sys.stdin.readlines()
data = ''.join(data)

# Parse json
data_json = json.loads(data)

# Rewind the polygons
data_rewinded = geojson_rewind.rewind(data_json)

# Print
# TODO: Pretty-print...
print(json.dumps(data_rewinded))
