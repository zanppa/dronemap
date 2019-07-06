# Introduction
This directory contains tools that help in generating the drone restriction maps.

* [airports.py](#airportspy) - Used to generate restriction zones around airport runways
* [ais-sup.pu](#ais-suppy) - Used to periodically fetch and parse AIS supplements for temporary restriction zones

## airports.py
This tool creates a geojson polygon list of restriction zones around airport runways.

The source data is `lentokentat.json` (airports) which contains array of airports, their IDs, center point and 
width and endpoints of each runway. The coordinates are in WGS84 and width is in meters.

The script generates circles of given diameter (e.g. 1 km or 3 km) at multiple points along the length of the runway(s) and then 
combines all the circles to one polygon.

The following example shows two restriction zones for EFHK built using the script. The inner one is at 1 km from the 
runways and the second one is at 3 km from the runways. The zones are single polygon each.

![Example restriction zones for EFHK](https://github.com/zanppa/dronemap/raw/master/tools/efhk_restriction.PNG)

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
 --file         output file name, default --file=sup.geojson
 --types        feature types to export, e.g. --file=RD (restricted, danger), R (only restriction zones), D (only danger zoner)
 --fetch        fetch new sup files interval, hours, eg. --fetch=24
 --update       update the geojson file interval, hours, e.g. --update=1
 --no-active    do no create features for currently active regions
 --no-passed    do no create features for passed regions
 --no-pending   do no create features for pending (valid in future) regions
 -v, --verbose, verbose output, add multiple for more info
 ```
By default the tool outputs all restriction zones regardless of whether they are currently active, passed or in the future. The 
AIS wepage is fetched every 12 hours and the geojson is updated every 1 hour.

## lentokentat.json
lentokentat.json is the source data used to generate restriction zones around airports, see [airports.py](#airportspy). The file is a dictionary containing one key `airports` which is an array of airports. All the airports have following structure:
```
{
  "id":"EFPO",
  "name":"Pori",
  "date":"24.5.2018",
  "updated":"12.8.2018",
  "center":[21.7977777778,61.4613888889],
  "runways":{
    "12/30":{"width":60,"length":2351,"end1":[21.7813444444,61.4681138889],"end2":[21.8171194444,61.455775]},
    "17/35":{"width":30,"length":801,"end1":[21.7984777778,61.4639777778],"end2":[21.8000777778,61.4568305556]}}
}
```
where `id`is the identification of the airport, `name` is the human readable name, `date` is the date the information was last checked (from the source data at AIS), `updated` is the date when the pdf file in the AIS webpage was updated, `center` contains array of longitude, latitude in WGS84, and `runways`is a dictionary of all the runways of the airport.

The `runways` dictionary has the runway name as the key (e.g. `12/30` which is the heading of the runway, 120 degrees or 300 degrees depending on the direction). For each runway following variables are given: `width` is the runway width in meters, `length` is the runway length in meters, `end1` is longitude, latitude of one end of the runway and `end2`is the longitude, latitude of the other end.
