#!/bin/bash

curl -k -XGET 'https://www.openstreetmap.org/api/0.6/map?bbox=2.32544%2C48.88745%2C2.32573%2C48.88758' \
    > tests/resources/small.osm
