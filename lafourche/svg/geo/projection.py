from abc import ABC, abstractmethod


class Projection(ABC):
    """Project a geo-point (lat, lon) onto an orthogonal coordinate system

    The projected coordinates should be an integer tuple, because it is then used to draw lines onto the svg canvas.
    """

    @abstractmethod
    def project(self, longitude: float, latitude: float) -> (int, int):
        pass

    @abstractmethod
    def canvas_size(self) -> (int, int):
        pass
