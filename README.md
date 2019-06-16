# dronemap
A database and simple interface to show Finland's drone restriction zones on a map

## Introduction
This repository contains geojson files for drone restriction zones of Finland.
The files are hand-crafted from freely available data from [AIP Suomi/Finland](https://www.ais.fi/ais/aip/fi/index.htm)
Note that the restriction zones are not complete and may not be up to date anymore.

## Files
Following files are included in the repository:

* index.html: example file which loads the restriction zones and displays them over Openstreetmap
* lentokentat.geojson: Prohibited zones near airports (runways)
* valvottu.geojson: Controlled airspace areas (near airports), drone restrictions apply
* rajoitukset.geojson: Other restriction zones (military zones etc), typically no-fly zones
* lennatyspaikat.geojson: Special drone flying areas
* lentokentat.json: Airport and runway data for generation of the prohibited zones
* circle2.py: Generates the prohibited zones near runways using lentokentat.json as the source
