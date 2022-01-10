import logging

from .parser import OsmParser
from .svg import SimpleSvgGenerator

if __name__ == '__main__':
    logging.basicConfig(filename='lafourche.log', level=logging.DEBUG)

    print("Downloading file")
    # TODO(gb): Add capability to download file directly from coordinates
    input_osm_file = ""

    logging.info("Parsing file")
    parser = OsmParser()
    internal_map = parser.parse(input_osm_file)

    logging.info("Writing svg")
    svg_writer = SimpleSvgGenerator()
    output_file = svg_writer.generate(internal_map)

    logging.info("Map successfully exported @ " + output_file)
