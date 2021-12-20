import logging
import tempfile

import svgwrite

from .geo.naiveprojection import Projection, NaiveProjection
from .svggenerator import SvgGenerator
from ..model import Map


class SimpleSvgGenerator(SvgGenerator):
    """Generate an SVG printing lines one by one on the canvas"""

    logger = logging.getLogger(__name__)

    __CANVAS_WIDTH = 256
    __COLOR = svgwrite.rgb(0, 0, 0)

    @staticmethod
    def create() -> SvgGenerator:
        return SimpleSvgGenerator()

    def generate(self, map_to_export: Map) -> str:
        projection = self.__get_projection(map_to_export)

        temporary_file = tempfile.mktemp(suffix='.svg')
        self.logger.debug("Temporary file name %s", temporary_file)
        drawing = svgwrite.Drawing(filename=temporary_file, size=projection.canvas_size())

        for edge in map_to_export:
            from_point = projection.project(edge.node1.latitude, edge.node1.longitude)
            to_point = projection.project(edge.node2.latitude, edge.node2.longitude)

            self.logger.debug("Adding line to canvas from (%s) to (%s) (weight %s)", from_point, to_point, edge.weight)
            line = drawing.line(from_point, to_point, stroke=self.__COLOR, stroke_width=edge.weight)
            drawing.add(line)

        drawing.save()
        return temporary_file

    def __get_projection(self, map_to_export: Map) -> Projection:
        return NaiveProjection.create(self.__CANVAS_WIDTH,
                                      map_to_export.get_bottom_left(),
                                      map_to_export.get_top_right())
