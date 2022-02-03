import logging
import os.path
import tempfile
import unittest
import xml.etree.ElementTree as ElementTree

from lafourche.parser import OsmParser


class TestOsmParser(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def test_get_weight_for_way_highway_pedestrian(self):
        parser = OsmParser()

        xml = """
        <way id="819897361" visible="true" version="2" changeset="93977993" uid="963055">
          <nd ref="27323728"/>
          <nd ref="6121940144"/>
          <nd ref="5715654115"/>
          <tag k="busway:left" v="opposite_lane"/>
          <tag k="highway" v="primary"/>
          <tag k="lit" v="yes"/>
          <tag k="maxspeed" v="30"/>
         </way>
        """
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(xml)
        way = ElementTree.parse(tmp)
        weight = parser.get_weight_for_way(way)

        self.assertEqual(4, weight, "Expected weight 4 for primary highway")

    def test_get_weight_for_way_highway_unknown(self):
        parser = OsmParser()

        xml = """
        <way id="819897361" visible="true" version="2" changeset="93977993" uid="963055">
          <nd ref="27323728"/>
          <nd ref="6121940144"/>
          <nd ref="5715654115"/>
          <tag k="busway:left" v="opposite_lane"/>
          <tag k="highway" v="unknown"/>
          <tag k="lit" v="yes"/>
          <tag k="maxspeed" v="30"/>
         </way>
        """
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(xml)
        way = ElementTree.parse(tmp)
        weight = parser.get_weight_for_way(way)

        self.assertEqual(-1, weight, "Expected weight -1 for primary unknown")

    def test_get_weight_for_way_highway_multiple(self):
        parser = OsmParser()

        xml = """
        <way id="819897361" visible="true" version="2" changeset="93977993" uid="963055">
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
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(xml)
        way = ElementTree.parse(tmp)
        weight = parser.get_weight_for_way(way)

        self.assertEqual(3, weight, "Expected weight 3 for secondary highway")

    def test_get_weight_for_no_highway(self):
        parser = OsmParser()

        xml = """
        <way id="819897361" visible="true" version="2" changeset="93977993" uid="963055">
          <nd ref="27323728"/>
          <nd ref="6121940144"/>
          <nd ref="5715654115"/>
          <tag k="busway:left" v="opposite_lane"/>
          <tag k="lit" v="yes"/>
          <tag k="maxspeed" v="30"/>
         </way>
        """
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(xml)
        way = ElementTree.parse(tmp)
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
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(xml)
        node = ElementTree.parse(tmp)
        node_registry = parser.get_node_registry(node)

        self.assertEqual(3, node_registry.__len__(), "Expected 3 nodes")

    def test_get_node_registry_no_id(self):
        parser = OsmParser()

        xml = """
            <osm version="0.6" copyright="OpenStreetMap and contributors">
                <bounds minlat="48.8874500" minlon="2.3254400" maxlat="48.8875800" maxlon="2.3257300"/>
                <node visible="true" version="9" uid="6848" lat="48.8880344" lon="2.3246333"/>
                <node id="27323728" visible="true" uid="37548" lat="48.8874983" lon="2.3255897"/>
                <node id="27323735" visible="true" uid="6848" lat="48.8871648" lon="2.3257420"/>
            </osm>
        """
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(xml)
        node = ElementTree.parse(tmp)
        node_registry = parser.get_node_registry(node)

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
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(xml)
        node = ElementTree.parse(tmp)
        node_registry = parser.get_node_registry(node)

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
        tmp = tempfile.NamedTemporaryFile()
        with open(tmp.name, 'w') as f:
            f.write(xml)
        node = ElementTree.parse(tmp)
        node_registry = parser.get_node_registry(node)

        self.assertEqual(0, node_registry.__len__(), "Expected 0 nodes")

    def test_parse(self):
        osm_map = os.path.join(os.path.dirname(__file__), "../resources/small.osm")

        parser = OsmParser.create()
        map_result = parser.parse(osm_map)

        self.assertEqual(map_result.__len__(), 18, "Expected 18 edges on the map")
