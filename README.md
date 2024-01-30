# 🌏 osmplaces readme:

## Installation:
Use `pipx install .` in the `osmplaces` repository. That's it!

## Usage and Arguments:

`osmplaces` is a simple a small tool to extract all names (in every language) associated with a place in the XML output of an `osmosis` command. The use case that `osmplaces` was written to consider was *only* the output of this command in the example. Any other commands including other OSM tags may fail. For dependencies (mainly Java) and proper usage of Osmosis, please see the [Osmosis Beginner's Guide](https://wiki.openstreetmap.org/wiki/Osmosis#Beginner's_guide) on the OSM Wiki.
## Example:

For example, using the [pitcairn-islands-latest.osm.pbf](https://download.geofabrik.de/australia-oceania/pitcairn-islands-latest.osm.pbf) on GeoFabrik:

```Bash
osmosis --read-pbf file="pitcarin-islands-latest.osm.pbf" \
        --tf accept-nodes place=city,town,village,hamlet \
        --tf accept-nodes "name=*" \
        --tf reject-ways \
        --tf reject-relations \
        --write-xml pitcairn-islands-places.osm
```

This produces an XML file like the following:

```XML
<?xml version='1.0' encoding='UTF-8'?>
<osm version="0.6" generator="Osmosis 0.48.3">
  <bounds minlon="-133.06643" minlat="-27.66403" maxlon="-118.34477" maxlat="-21.59613" origin="0.48.3"/>
  <node id="2134592841" version="20" timestamp="2023-07-21T00:17:53Z" uid="0" user="" lat="-25.066667" lon="-130.100205">
    <tag k="capital" v="yes"/>
    <tag k="geonameid" v="4030723"/>
    <tag k="name" v="Adamstown"/>
    <tag k="name:ar" v="آدمزتاون"/>
    <tag k="name:az" v="Adamstaun"/>
    <tag k="name:bg" v="Адамстаун"/>
    ...
  </node>
</osm>
```

Running `osmplaces -i pitcairn-islands-places.osm -o data/` produces a `data/` directory where there is a .json file for the names and places for every language included in the original `pitcairn-islands-latest.osm.pbf` file:
```
> $ ls -l | awk '{print $9}'
output_nodes_ar.json
output_nodes_az.json
output_nodes_bg.json
output_nodes_da.json
output_nodes_de.json
output_nodes_en.json
output_nodes_es.json
output_nodes_et.json
(etc) ...
```
Inside each .json file, you are given the name, the latitude and longitude, and the ID of the OSM node reference ID:
```json
[
    {
        "id": "2134592841",
        "lat": "-25.066667",
        "lon": "-130.100205",
        "name": "Adamstown"
    }
]
```
