import pytest
from lxml import etree
from py_opendrive.geometries.line import Line


def test_line_from_xml_and_to_xml_roundtrip():
    # Example XML string for OpenDRIVE geometry with line
    xml_data = """
    <geometry s="0.0" x="100.0" y="200.0" hdg="0.5" length="50.0">
    </geometry>
    """

    elem = etree.fromstring(xml_data)

    # Decode from XML.
    line = Line.from_xml(elem)

    # Check that attributes were parsed correctly.
    assert pytest.approx(line.s) == 0.0
    assert pytest.approx(line.x) == 100.0
    assert pytest.approx(line.y) == 200.0
    assert pytest.approx(line.hdg) == 0.5
    assert pytest.approx(line.length) == 50.0

    # Encode back to XML.
    elem_out = line.to_xml()

    # Validate structure and attributes.
    assert elem_out.tag == "geometry"
    assert elem_out.get("s") == "0.0"
    assert elem_out.get("x") == "100.0"
    assert elem_out.get("y") == "200.0"
    assert elem_out.get("hdg") == "0.5"
    assert elem_out.get("length") == "50.0"

    # Roundtrip check.
    line_roundtrip = Line.from_xml(elem_out)
    assert line == line_roundtrip
