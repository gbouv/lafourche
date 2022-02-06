

class Geopoint:
    lon: float
    lat: float

    def __init__(self, longitude: float, latitude: float):
        self.lat = latitude
        self.lon = longitude

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Geopoint):
            return False
        return o.lon == self.lon and o.lat == self.lat

    def __repr__(self) -> str:
        return "Geopoint(lon: " + str(self.lon) + ", lat: " + str(self.lat) + ")"
