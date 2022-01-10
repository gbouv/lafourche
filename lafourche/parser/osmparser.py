import logging
import xml.etree.ElementTree as ElementTree

from .parser import Parser
from ..model import Map, Node


class OsmParser(Parser):
    logger = logging.getLogger(__name__)

    @staticmethod
    def create() -> Parser:
        return OsmParser()

    def parse(self, filepath: str) -> Map:
        """Parser for an .osm file (export from openstreetmap.org)"""
        self.logger.debug("Parsing file %s", filepath)

        tree = ElementTree.parse(filepath)
        node_registry = self.__get_node_registry(tree.getroot())

        edges = self.__get_edges(tree.getroot(), node_registry)

        return Map(edges)

    def __get_node_registry(self, tree_root: ElementTree) -> {int: Node}:
        """Returns a dictionary of node ID -> Node object"""
        node_registry = {}
        for node in tree_root.iter('node'):
            # TODO(mv): implement
            self.logger.debug("Reading %s (%s, %s, %s)", node.tag, node.attrib.get('id'), node.attrib.get('lat'),
                              node.attrib.get('lon'))
            node_registry[node.attrib.get('id')] = Node(node.attrib.get('id'), node.attrib.get('lat'),
                              node.attrib.get('lon'))
        return node_registry

    def __get_edges(self, tree_root: ElementTree, node_registry: {int: Node}) -> []:
        """Returns a list of edges, keeping only the useful ones"""
        for way in tree_root.iter('way'):
            # TODO(mv): implement
            self.logger.debug("Reading %s (%s)", way.tag, way.attrib)
            for nodeRef in way.iter('nd'):
                self.logger.debug("Reading %s (%s)", nodeRef.tag, nodeRef.attrib.get('ref'))
        return []
