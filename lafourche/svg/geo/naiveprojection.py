import logging
import math

from .projection import Projection


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
    __bottom_left_lon: float
    __bottom_left_lat: float
    __top_right_lon: float
    __top_right_lat: float

    def __init__(self, canvas_size: (int, int), bottom_left_geopoint: (float, float),
                 top_right_geopoint: (float, float)):
        self.__width = canvas_size[0]
        self.__height = canvas_size[1]
        self.__bottom_left_lon = bottom_left_geopoint[0]
        self.__bottom_left_lat = bottom_left_geopoint[1]
        self.__top_right_lon = top_right_geopoint[0]
        self.__top_right_lat = top_right_geopoint[1]

    @staticmethod
    def create(canvas_width: int, bottom_left_geopoint: (float, float),
               top_right_geopoint: (float, float)) -> Projection:
        canvas_size = (canvas_width,
                       NaiveProjection.get_canvas_height(canvas_width, bottom_left_geopoint, top_right_geopoint))
        return NaiveProjection(canvas_size, bottom_left_geopoint, top_right_geopoint)

    def project(self, longitude: float, latitude: float) -> (int, int):
        self.__validate(longitude, latitude)
        abscissa = self.__get_abscissa(longitude)
        ordinate = self.__get_ordinate(latitude)
        self.logger.debug("Converting (%s; %s) into (%s; %s)", longitude, latitude, abscissa, ordinate)
        return abscissa, ordinate

    def canvas_size(self) -> (int, int):
        return self.__width, self.__height

    def __validate(self, longitude: float, latitude: float):
        if longitude < self.__bottom_left_lon or longitude > self.__top_right_lon \
                or latitude < self.__bottom_left_lat or latitude > self.__top_right_lat:
            raise ValueError("Coordinate Out of Range")

    def __get_abscissa(self, longitude: float) -> int:
        center_lon = (self.__top_right_lon + self.__bottom_left_lon) / 2
        return round((longitude - center_lon) / (self.__top_right_lon - self.__bottom_left_lon) * self.__width)

    def __get_ordinate(self, latitude: float) -> int:
        center_lat = (self.__top_right_lat + self.__bottom_left_lat) / 2
        return round((latitude - center_lat) / (self.__top_right_lat - self.__bottom_left_lat) * self.__height)

    @staticmethod
    def get_canvas_height(canvas_width: int, bottom_left_geopoint: (float, float),
                          top_right_geopoint: (float, float)) -> int:
        height_width_ratio = (top_right_geopoint[1] - bottom_left_geopoint[1]) / (top_right_geopoint[0] - bottom_left_geopoint[0])
        return math.ceil(canvas_width * height_width_ratio)
