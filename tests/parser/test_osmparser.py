import logging
import os.path
import tempfile
import unittest
import xml.etree.ElementTree as ElementTree

from lafourche.parser import OsmParser


class TestOsmParser(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    @staticmethod
    def get_elementtree_from_xml(xml):
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(xml)
        return ElementTree.parse(tmp)

    def test_get_weight_for_way_highway_primary(self):
        parser = OsmParser()

        xml = """
        <way id="819897361" visible="true" version="2" uid="963055">
          <nd ref="27323728"/>
          <nd ref="6121940144"/>
          <nd ref="5715654115"/>
          <tag k="busway:left" v="opposite_lane"/>
          <tag k="highway" v="primary"/>
          <tag k="lit" v="yes"/>
          <tag k="maxspeed" v="30"/>
         </way>
        """
        way = self.get_elementtree_from_xml(xml).getroot()
        weight = parser.get_weight_for_way(way)

        self.assertEqual(10, weight, "Expected weight 10 for primary highway")

    def test_get_weight_for_way_highway_unknown(self):
        parser = OsmParser()

        xml = """
        <way id="819897361" visible="true" version="2" uid="963055">
          <nd ref="27323728"/>
          <nd ref="6121940144"/>
          <nd ref="5715654115"/>
          <tag k="busway:left" v="opposite_lane"/>
          <tag k="highway" v="unknown"/>
          <tag k="lit" v="yes"/>
          <tag k="maxspeed" v="30"/>
         </way>
        """
        way = self.get_elementtree_from_xml(xml).getroot()
        weight = parser.get_weight_for_way(way)

        self.assertEqual(-1, weight, "Expected weight -1 for unknown highway")

    def test_get_weight_for_way_highway_multiple(self):
        parser = OsmParser()

        xml = """
        <way id="819897361" visible="true" version="2" uid="963055">
          <nd ref="27323728"/>
          <nd ref="6121940144"/>
          <nd ref="5715654115"/>
          <tag k="busway:left" v="opposite_lane"/>
          <tag k="highway" v="secondary"/>
          <tag k="highway" v="pedestrian"/>
          <tag k="highway" v="unknown"/>
          <tag k="lit" v="yes"/>
          <tag k="maxspeed" v="30"/>
         </way>
        """
        way = self.get_elementtree_from_xml(xml).getroot()
        weight = parser.get_weight_for_way(way)

        self.assertEqual(10, weight, "Expected weight 10 for secondary highway")

    def test_get_weight_for_no_highway(self):
        parser = OsmParser()

        xml = """
        <way id="819897361" visible="true" version="2" uid="963055">
          <nd ref="27323728"/>
          <nd ref="6121940144"/>
          <nd ref="5715654115"/>
          <tag k="busway:left" v="opposite_lane"/>
          <tag k="lit" v="yes"/>
          <tag k="maxspeed" v="30"/>
         </way>
        """
        way = self.get_elementtree_from_xml(xml).getroot()
        weight = parser.get_weight_for_way(way)

        self.assertEqual(-1, weight, "Expected weight -1 for no highway")

    def test_get_node_registry_success(self):
        parser = OsmParser()

        xml = """
            <osm version="0.6" copyright="OpenStreetMap and contributors">
                <bounds minlat="48.8874500" minlon="2.3254400" maxlat="48.8875800" maxlon="2.3257300"/>
                <node id="27323684" visible="true" version="9" uid="6848" lat="48.8880344" lon="2.3246333"/>
                <node id="27323728" visible="true" version="23" uid="37548" lat="48.8874983" lon="2.3255897"/>
                <node id="27323735" visible="true" version="28" uid="6848" lat="48.8871648" lon="2.3257420"/>
            </osm>
        """
        tree_root = self.get_elementtree_from_xml(xml)
        node_registry = parser.get_node_registry(tree_root)

        self.assertEqual(3, node_registry.__len__(), "Expected 3 nodes")

    def test_get_node_registry_no_id(self):
        parser = OsmParser()

        xml = """
            <osm version="0.6" copyright="OpenStreetMap and contributors">
                <bounds minlat="48.8874500" minlon="2.3254400" maxlat="48.8875800" maxlon="2.3257300"/>
                <node visible="true" version="9" uid="6848" lat="48.8880344" lon="2.3246333"/>
                <node id="27323728" visible="true" version="23" uid="37548" lat="48.8874983" lon="2.3255897"/>
                <node id="27323735" visible="true" version="28" uid="6848" lat="48.8871648" lon="2.3257420"/>
            </osm>
        """
        tree_root = self.get_elementtree_from_xml(xml)
        node_registry = parser.get_node_registry(tree_root)

        self.assertEqual(2, node_registry.__len__(), "Expected 2 nodes")

    def test_get_node_registry_no_lat(self):
        parser = OsmParser()

        xml = """
            <osm version="0.6" copyright="OpenStreetMap and contributors">
                <bounds minlat="48.8874500" minlon="2.3254400" maxlat="48.8875800" maxlon="2.3257300"/>
                <node visible="true" version="9" uid="6848" lat="48.8880344" lon="2.3246333"/>
                <node id="27323728" visible="true" version="23" uid="37548" lon="2.3255897"/>
                <node id="27323735" visible="true" version="28" uid="6848" lat="48.8871648" lon="2.3257420"/>
            </osm>
        """
        tree_root = self.get_elementtree_from_xml(xml)
        node_registry = parser.get_node_registry(tree_root)

        self.assertEqual(1, node_registry.__len__(), "Expected 1 nodes")

    def test_get_node_registry_no_lon(self):
        parser = OsmParser()

        xml = """
            <osm version="0.6" copyright="OpenStreetMap and contributors">
                <bounds minlat="48.8874500" minlon="2.3254400" maxlat="48.8875800" maxlon="2.3257300"/>
                <node visible="true" version="9" uid="6848" lat="48.8880344" lon="2.3246333"/>
                <node id="27323728" visible="true" version="23" uid="37548" lon="2.3255897"/>
                <node id="27323735" visible="true" version="28" uid="6848" lat="48.8871648"/>
            </osm>
        """
        tree_root = self.get_elementtree_from_xml(xml)
        node_registry = parser.get_node_registry(tree_root)

        self.assertEqual(0, node_registry.__len__(), "Expected 0 nodes")

    def test_get_edges_not_in_registry(self):
        parser = OsmParser()
        node_registry = {
            "27323728": ("27323728", 50, -110),
            "6121940144": ("6121940144", 3, 25),
            "3": ("3", 5, 15),
        }
        xml = """
        <way id="819897361" visible="true" version="2" uid="963055">
          <nd ref="27323728"/>
          <nd ref="6121940144"/>
          <nd ref="5715654115"/>
          <tag k="busway:left" v="opposite_lane"/>
          <tag k="highway" v="primary"/>
          <tag k="lit" v="yes"/>
          <tag k="maxspeed" v="30"/>
         </way>
        """
        tree_root = self.get_elementtree_from_xml(xml)
        edges = parser.get_edges(tree_root, node_registry)
        self.assertEqual(1, edges.__len__(), "Expected 1 edges")

    def test_parse(self):
        osm_map = os.path.join(os.path.dirname(__file__), "../resources/small.osm")

        parser = OsmParser.create()
        map_result = parser.parse(osm_map)
        self.assertEqual(map_result.__len__(), 18, "Expected 18 edges on the map")
