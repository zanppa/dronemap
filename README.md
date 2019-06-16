# dronemap
A database and simple interface to show Finland's drone restriction zones on a map

## Introduction
This repository contains geojson files for drone restriction zones of Finland.
The files are hand-crafted from freely available data from [AIP Suomi/Finland](https://www.ais.fi/ais/aip/fi/index.htm)
Note that the restriction zones are not complete and are already outdated.

## Background
DroneInfo mobile app can be used to display the restriction zones, however [the website](https://www.droneinfo.fi/) only shows some restriction zones. Also I found the mobile app too crowded because it also shows some unnecessary layers. So I did my own version.

I ended up typing most of the restriction zones by hand from pdf file to geojson format. I did not find any (free/open) data source that could be used for this. I also wrote a python script to generate restriction zones which are measured from runway edges, for this I created a json file with all runways by hand.

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
* This data is **OUTDATED** because the rules have changed 7.12.2018. [The new regulation is here](https://www.finlex.fi/data/normit/44667/TRAFI_334638_03040000_2017_Use_of_remotely_piloted_aircraft__1_.pdf)
* At the moment it seems that github does not render html (even with the ```raw``` view) and does not allow remote ajax data fetching (e.g. from github.io).
* DroneInfo app seems to be updated to have much clearer map and also show some more restriction areas that are not included in this version.

