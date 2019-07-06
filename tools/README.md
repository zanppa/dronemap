# Introduction
This directory contains tools that help in generating the drone restriction maps.

* [airports.py](#airports.py) - Used to generate restriction zones around airport runways
* [ais-sup.pu](#ais-sup.py) - Used to periodically fetch and parse AIS supplements for temporary restriction zones

## airports.py
This tool creates a geojson polygon list of restriction zones around airport runways.

The source data is `lentokentat.json` (airports) which contains array of airports, their IDs, center point and 
width and endpoints of each runway. The coordinates are in WGS84 and width is in meters.

The script generates circles of given diameter (e.g. 1 km or 3 km) at multiple points along the length of the runway(s) and then 
combines all the circles to one polygon.

The included source data is hand crafted from publicly available [AIS AIP (Fi)](https://www.ais.fi/ais/aip/fi/index.htm), [AIS AIP (En)](https://www.ais.fi/ais/aip/en/index.htm) 
data, textpage of each airport, e.g. [Helsinki-Vantaa EFHK](https://www.ais.fi/ais/aip/ad/efhk/EF_AD_2_EFHK_EN.pdf).

## ais-sup.py
[AIS](https://www.ais.fi/fi) publishes [supplements](https://www.ais.fi/ais/aipsup/AipSup.htm) on their webpage in pdf format. The 
supplements temporarily change the contents of the [AIP](https://www.ais.fi/ais/aip/fi/index.htm).

Some pdf files of the supplements have embedded xml file(s), which contain e.g. temporary restriction zone 
definitions. These xml files are easily parsed and the restriction zone polygons together with their validity time can be parsed.

This tool periodically checks the AIS SUP webpage for new pdf files, downloads them and parses the included xml file(s). It
also periodically checks which zones are valid (by their timestamp) and writes out a geojson file which includes all valid 
restriction zones.

The tool has multiple options for configuring the output. The basic command line is:
`python ais_sup.py --file=sup.geojson`
with following options possible
```
 --file         output file name, default=sup.geojson
 --types        feature types to export, e.g. RD (restricted, danger)
 --fetch        fetch new sup files interval, hours
 --update       update the geojson file interval, hours
 --no-active    do no create features for currently active regions
 --no-passed    do no create features for passed regions
 --no-pending   do no create features for pending (valid in future) regions
 -v, --verbose, verbose output, add multiple for more info
 ```
