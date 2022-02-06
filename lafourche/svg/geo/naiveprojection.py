import logging
import math

from .projection import Projection
from ...model.geopoint import Geopoint


class NaiveProjection(Projection):
    """Naive coordinate projection. Each geo coordinate is projected by doing a simple ratio of its latitude /
    longitude.

    All coordinates are projected into a rectangle defined by:
    top_left_coord = (0 ; 0)
    top_right_coord = (__width ; 0)
    bottom_left_coord = (0 ; __height)
    bottom_right_coord = (__width ; __height)

    The height and width of the canvas is computed using a constant number of pixels per meter
    """

    logger = logging.getLogger(__name__)

    # canvas size
    __px_per_deg = 100_000  # 0.01 deg -> 1000 px at the equator
    __height: int
    __width: int

    # area boundaries
    __bottom_left: Geopoint
    __top_right: Geopoint

    def __init__(self, canvas_size: (int, int), bottom_left_geopoint: Geopoint, top_right_geopoint: Geopoint):
        self.__width = canvas_size[0]
        self.__height = canvas_size[1]
        self.__bottom_left = bottom_left_geopoint
        self.__top_right = top_right_geopoint

    @staticmethod
    def create(bottom_left_geopoint: Geopoint, top_right_geopoint: Geopoint) -> Projection:
        canvas_size = NaiveProjection.get_canvas_size(bottom_left_geopoint, top_right_geopoint)
        return NaiveProjection(canvas_size, bottom_left_geopoint, top_right_geopoint)

    def project(self, geopoint: Geopoint) -> (int, int):
        self.__validate(geopoint)
        abscissa = self.__get_abscissa(geopoint.lon)
        ordinate = self.__get_ordinate(geopoint.lat)
        self.logger.debug("Converting (%s; %s) into (%s; %s)", geopoint.lon, geopoint.lat, abscissa, ordinate)
        return abscissa, ordinate

    def canvas_size(self) -> (int, int):
        return self.__width, self.__height

    def __validate(self, geopoint: Geopoint):
        if geopoint.lon < self.__bottom_left.lon or geopoint.lon > self.__top_right.lon \
                or geopoint.lat < self.__bottom_left.lat or geopoint.lat > self.__top_right.lat:
            raise ValueError("Coordinate Out of Range")

    def __get_abscissa(self, longitude: float) -> int:
        return round((longitude - self.__bottom_left.lon) / (self.__top_right.lon - self.__bottom_left.lon)
                     * self.__width)

    def __get_ordinate(self, latitude: float) -> int:
        return round((self.__top_right.lat - latitude) / (self.__top_right.lat - self.__bottom_left.lat)
                     * self.__height)

    @staticmethod
    def get_canvas_size(bottom_left_geopoint: Geopoint, top_right_geopoint: Geopoint) -> (int, int):
        height = (top_right_geopoint.lat - bottom_left_geopoint.lat) * NaiveProjection.__px_per_deg

        avg_lat = (top_right_geopoint.lat + bottom_left_geopoint.lat) / 2
        # for the longitude, __px_per_deg is applicable at the equator. The longitude needs to be "corrected" based on
        # the average latitude of the zone
        longitude_correction_factor = math.cos(avg_lat * math.pi / 180)
        width = (top_right_geopoint.lon - bottom_left_geopoint.lon) * NaiveProjection.__px_per_deg \
            * longitude_correction_factor

        return math.ceil(width), math.ceil(height)
