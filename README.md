# dronemap
A database and simple interface to show Finland's drone restriction zones on a map

## Introduction
This repository contains geojson files for drone restriction zones of Finland.
The files are hand-crafted from freely available data from [AIP Suomi/Finland](https://www.ais.fi/ais/aip/fi/index.htm)
Note that the restriction zones are not complete and may not be up to date anymore.

## Background
DroneInfo mobile app can be used to display the restriction zones, however [the website](https://www.droneinfo.fi/) only shows some restriction zones. Also I found the mobile app too crowded because it also shows some unnecessary layers. So I did my own version.

I ended up typing the restriction zones by hand from pdf file to geojson format. I did not find any (free/open) data source that could be used for this. This means that the zones may be already outdated.

## Files
Following files are included in the repository:

* index.html: example file which loads the restriction zones and displays them over Openstreetmap
* lentokentat.geojson: Prohibited zones near airports (runways)
* valvottu.geojson: Controlled airspace areas (near airports), drone restrictions apply
* rajoitukset.geojson: Other restriction zones (military zones etc), typically no-fly zones
* lennatyspaikat.geojson: Special drone flying areas
* lentokentat.json: Airport and runway data for generation of the prohibited zones
* circle2.py: Generates the prohibited zones near runways using lentokentat.json as the source


## Notes
* At the moment it seems that github does not render html (even with the ```raw``` view) and does not allow remote ajax data fetching (e.g. from github.io).
* DroneInfo app seems to be updated to have much clearer map and also show some more restriction areas that are not included in this version.
* DroneInfo app shows 1 km and 3 km areas near airports, maybe the 5 km rule has changed lately?
