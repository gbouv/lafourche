import logging
import xml.etree.ElementTree as ElementTree

from .parser import Parser
from ..model import Map, Node, Edge
from ..model.geopoint import Geopoint


class OsmParser(Parser):
    logger = logging.getLogger(__name__)
    __way_config = {
            'highway': {
                'motorway': 10,
                'trunk': 10,
                'primary': 10,
                'secondary': 10,
                'tertiary': 10,
                'unclassified': 10,
                'residential': 10,
                'service': 10,
                'motorway_link': 5,
                'trunk_link': 5,
                'primary_link': 5,
                'secondary_link': 5,
                'motorway_junction': 5,
                'living street': 5,
                'pedestrian': 5,
                'track': 5,
                'bus guideway': 5,
                'busway': 5,
                'raceway': 5,
                'road': 5,
                'construction': 5,
                'escape': 5,
                'footway': 1,
                'cycleway': 1,
                'bridleway': 1,
                'path': 1,
                'steps': 1,
            },
        }

    @staticmethod
    def create() -> Parser:
        return OsmParser()

    def parse(self, filepath: str) -> Map:
        """Parser for an .osm file (export from openstreetmap.org)"""
        self.logger.debug("Parsing file %s", filepath)

        tree = ElementTree.parse(filepath)
        node_registry = self.get_node_registry(tree.getroot())

        edges = self.get_edges(tree.getroot(), node_registry)

        return Map(edges)

    def get_node_registry(self, tree_root: ElementTree) -> {int: Node}:
        """Returns a dictionary of node ID -> Node object"""
        node_registry = {}
        for node in tree_root.iter('node'):
            self.logger.debug("Reading %s (%s, %s, %s)", node.tag, node.attrib.get('id'), node.attrib.get('lat'),
                              node.attrib.get('lon'))
            try:
                node_id = int(node.attrib.get('id'))
                node_lon = float(node.attrib.get('lon'))
                node_lat = float(node.attrib.get('lat'))
            except (ValueError, TypeError) as ex:
                self.logger.warning("An attribute of the node %s could not be parsed to a valid value (%s, %s, %s) %s",
                                    node.tag, node.attrib.get('id'), node.attrib.get('lat'), node.attrib.get('lon'), ex)
                continue
            node_registry[node.attrib.get('id')] = Node(node_id, Geopoint(node_lon, node_lat))
        return node_registry

    def get_weight_for_way(self, way: ElementTree) -> int:
        """Returns a weight for each way based on its tags. A weight of -1 means that the edge should be ignored."""
        way_config = self.__way_config
        weight = -1
        for tag in way.iter('tag'):
            tag_key = tag.attrib.get('k')
            tag_value = tag.attrib.get('v')
            if tag_key in way_config.keys():
                if tag_value in way_config[tag_key].keys():
                    weight = max(way_config[tag_key][tag_value], weight)
        self.logger.debug("weight for way %s = %s", way.attrib.get('id'), weight)
        if weight == -1:
            self.logger.debug("Way %s is not interesting. We do not keep it.", way.attrib.get('id'))
        return weight

    def get_edges(self, tree_root: ElementTree, node_registry: {int: Node}) -> []:
        """Returns a list of edges, keeping only the useful ones"""
        edges = []
        for way in tree_root.iter('way'):
            weight = self.get_weight_for_way(way)
            if weight > 0:
                i = 0
                node1 = None
                for nodeRef in way.iter('nd'):
                    self.logger.debug("Reading %s %s", nodeRef.tag, nodeRef.attrib.get('ref'))
                    if nodeRef.attrib.get('ref') not in node_registry.keys():
                        self.logger.error("Node %s is not in registry", nodeRef.attrib.get('ref'))
                    else:
                        node2 = node_registry[nodeRef.attrib.get('ref')]
                        if i != 0:
                            edge = Edge(node1, node2, weight)
                            edges.append(edge)
                            self.logger.debug("%s added", edge)
                        node1 = node2
                        i = i + 1

        return edges
