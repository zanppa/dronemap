This directory contains the geojson files for drone restriction zones. The files can be directly loaded using e.g. Openlayers.

The files included are:
* [lennatyspaikat.geojson](#lennatyspaikatgeojson)
* [lentokentat.geojson](#lentokentatgeojson)
* [rajoitukset.geojson](#rajoituksetgeojson)
* [sup.geojson](#supgeojson)
* [valvottu.geojson](#valvottugeojson)

## Format
All the files are in [geojson](https://geojson.org/) format and each file contains one `FeatureCollection`. In the collection, each feature represent one restriction zone (e.g. airport, controlled airspace) or flying place or similar. The `id` of each `Feature` is the identification of the feature, for example the airport ID (e.g. `EFHK`).

The `geometry` of each feature is either a polygon (for restriction zone) or a point (for flying place).

In addition to the id and geometry, each feature has several `properties`.  `name` is a human-readable name for the feature (e.g. airport name), `updated` is the date when the feature was last updated, `publ` is the date when the source data was published (according to the source data date when the feature was updated) and `type` is the type of the feature, which is currently one of the following:
```
R    Restricted, drone flying is prohibited completely
R2   Restricted, but flying is allowed near fixed obstacles and below them
L    Limited, controlled airspace. Maximum altitude 50 m
D    Danger zone (currently only in supplements)
A1   Official flying place, maximum altitude varies
A2   Official flying place in controlled airspace, maximum altitude 50 m
```

## lennatyspaikat.geojson
This file contains list of official drone (or RC) flying places.

## lentokentat.geojson
This file contains restriction zones near airports, i.e. near the runways. This file can be automatically generated by the tool 
included in the `tools` directory.

## rajoitukset.geojson
This file contains other restriction zones due to e.g. military operations or proximity to border.

## sup.geojson
This file contains the temporary zones from AIS supplements. This file can be automatically generated by the tool included 
in the `tools` directory.

## valvottu.geojson
This file contains the restricted areas in controlled airspace near airports.