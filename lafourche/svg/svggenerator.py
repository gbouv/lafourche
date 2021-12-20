from abc import ABC, abstractmethod

from ..model import Map


class SvgGenerator(ABC):
    """Converts a Map object into a svg file"""

    @abstractmethod
    def generate(self, map_to_export: Map) -> str:
        """Write the convent of the map to an SVG object and return the full path to the file"""
        pass
