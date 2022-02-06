#!/bin/bash

curl -k -XGET 'https://www.openstreetmap.org/api/0.6/map?bbox=2.32544%2C48.88745%2C2.32573%2C48.88758' \
    > tests/resources/small.osm
curl -k -XGET 'https://www.openstreetmap.org/api/0.6/map?bbox=2.3184%2C48.8846%2C2.3285%2C48.8935' \
    > tests/resources/big.osm
