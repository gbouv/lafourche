import logging


class GeohashConverter:
    """Decode a geohash into its corresponding lat/lon bounding box"""

    logger = logging.getLogger(__name__)

    __base32 = "0123456789bcdefghjkmnpqrstuvwxyz"

    def decode(self, geohash: str):
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

        result = [(min_lon, min_lat), (max_lon, max_lat)]
        self.logger.debug("Decoded geohash %s -> %s", geohash, result)
        return result
