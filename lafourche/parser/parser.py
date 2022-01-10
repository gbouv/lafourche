from abc import ABC, abstractmethod

from ..model import Map


class Parser(ABC):
    """A parser converts a file into a Map object"""

    @abstractmethod
    def parse(self, filepath: str) -> Map:
        """Read the file located at filepath and produces a Map object from it
        Note that this operation likely involves some filtering. Not all element from the initial file will be present
        in the resulting map:
        """
        pass
