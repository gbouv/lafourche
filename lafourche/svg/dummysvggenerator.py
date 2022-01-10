import logging

import svgwrite

from .svggenerator import SvgGenerator
from ..model import Map


class DummySvgGenerator(SvgGenerator):
    """Dummy SVG generator to test svgwrite methods"""
    logger = logging.getLogger(__name__)

    @staticmethod
    def create() -> SvgGenerator:
        return DummySvgGenerator()

    def generate(self, map_to_export: Map) -> str:
        temporary_file = 'test.svg'
        self.logger.debug("Temporary file name %s", temporary_file)
        drawing = svgwrite.Drawing(filename=temporary_file, size=(64, 32))
        drawing.add(drawing.line((10, 10), (20, 10), stroke=svgwrite.rgb(255, 0, 0)))
        drawing.add(drawing.line((10, 10), (10, 20), stroke=svgwrite.rgb(0, 255, 0)))
        drawing.add(drawing.line((10, 20), (20, 20), stroke=svgwrite.rgb(0, 0, 255)))
        drawing.add(drawing.line((20, 20), (20, 10), stroke=svgwrite.rgb(0, 0, 0), stroke_width=10))
        drawing.save(pretty=True)
        return temporary_file
