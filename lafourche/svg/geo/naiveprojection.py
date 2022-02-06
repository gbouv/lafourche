import logging
import math

from .projection import Projection
from ...model.geopoint import Geopoint


class NaiveProjection(Projection):
    """Most naive coordinate projection ever

    Project all coordinates into a rectangle defined by:
    top_left_coord = (- __width / 2 ; + __height / 2)
    top_right_coord = (+ __width / 2 ; + __height / 2)
    bottom_left_coord = (- __width / 2 ; - __height / 2)
    bottom_right_coord = (+ __width / 2 ; - __height / 2)

    Each geo coordinate is projected by doing a simple ratio of its latitude / longitude;
    """

    logger = logging.getLogger(__name__)

    # canvas size
    __height: int
    __width: int

    # area boundaries
    __bottom_left: Geopoint
    __top_right: Geopoint

    def __init__(self, canvas_size: (int, int), bottom_left_geopoint: Geopoint,
                 top_right_geopoint: Geopoint):
        self.__width = canvas_size[0]
        self.__height = canvas_size[1]
        self.__bottom_left = bottom_left_geopoint
        self.__top_right = top_right_geopoint

    @staticmethod
    def create(canvas_width: int, bottom_left_geopoint: Geopoint,
               top_right_geopoint: Geopoint) -> Projection:
        canvas_size = (canvas_width,
                       NaiveProjection.get_canvas_height(canvas_width, bottom_left_geopoint, top_right_geopoint))
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
        center_lon = (self.__top_right.lon + self.__bottom_left.lon) / 2
        return round((longitude - center_lon) / (self.__top_right.lon - self.__bottom_left.lon) * self.__width)

    def __get_ordinate(self, latitude: float) -> int:
        center_lat = (self.__top_right.lat + self.__bottom_left.lat) / 2
        return round((latitude - center_lat) / (self.__top_right.lat - self.__bottom_left.lat) * self.__height)

    @staticmethod
    def get_canvas_height(canvas_width: int, bottom_left_geopoint: Geopoint,
                          top_right_geopoint: Geopoint) -> int:
        height_width_ratio = (top_right_geopoint.lat - bottom_left_geopoint.lat)\
                             / (top_right_geopoint.lon - bottom_left_geopoint.lon)
        return math.ceil(canvas_width * height_width_ratio)
