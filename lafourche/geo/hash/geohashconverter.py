import logging

from lafourche.model.geopoint import Geopoint


class GeohashConverter:
    """Decode a geohash into its corresponding lat/lon bounding box"""

    logger = logging.getLogger(__name__)

    __base32 = "0123456789bcdefghjkmnpqrstuvwxyz"

    def decode(self, geohash: str) -> (Geopoint, Geopoint):
        self.logger.debug("Decoding geohash %s", geohash)

        min_lat = -90
        max_lat = 90
        min_lon = -180
        max_lon = 180

        lon_next = 1
        for c in geohash:
            try:
                char_index = self.__base32.index(c)
            except ValueError:
                self.logger.warning("Invalid character in geohash '%s' (geohash: '%s')", c, geohash)
                return None

            for i in range(4, -1, -1):  # for each of the five bytes in char_index
                if char_index >> i & 0b1:  # this is the value of the byte at index i
                    # if the byte at index i is 1, then we update the minimum
                    if lon_next:
                        min_lon = (max_lon + min_lon) / 2
                    else:
                        min_lat = (max_lat + min_lat) / 2
                else:
                    # if the byte at index i is 0, then we update the maximum
                    if lon_next:
                        max_lon = (max_lon + min_lon) / 2
                    else:
                        max_lat = (max_lat + min_lat) / 2
                lon_next = lon_next ^ 1

        result = Geopoint(min_lon, min_lat), Geopoint(max_lon, max_lat)
        self.logger.debug("Decoded geohash %s -> %s", geohash, result)
        return result

    def encode(self, coord: Geopoint, geohash_length: int) -> str:
        self.logger.debug("Encoding geo coordinate %s - geohash length %s", coord, geohash_length)

        min_lat = -90
        max_lat = 90
        min_lon = -180
        max_lon = 180

        lon_next = 1
        geohash = ""
        while len(geohash) < geohash_length:
            index = 0
            for i in range(0, 5):
                if lon_next:
                    middle = (max_lon + min_lon) / 2
                    if coord.lon > middle:
                        min_lon = middle
                        index = index << 1 | 1
                    else:
                        max_lon = middle
                        index = index << 1 | 0
                else:
                    middle = (max_lat + min_lat) / 2
                    if coord.lat > middle:
                        min_lat = middle
                        index = index << 1 | 1
                    else:
                        max_lat = middle
                        index = index << 1 | 0
                lon_next = lon_next ^ 1
            geohash = geohash + self.__base32[index]
        self.logger.debug("Encoded geo coordinate %s into %s", coord, geohash)
        return geohash
