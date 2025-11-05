import pytest
from lxml import etree
from py_opendrive.geometries.spiral import Spiral


def test_spiral_from_xml_and_to_xml_roundtrip():
    # Example XML string for OpenDRIVE geometry with spiral.
    xml_data = """
    <geometry s="0.0" x="100.0" y="200.0" hdg="0.5" length="50.0">
        <spiral curvStart="0.0" curvEnd="0.02" />
    </geometry>
    """

    elem = etree.fromstring(xml_data)

    # Decode from XML.
    spiral = Spiral.from_xml(elem)

    # Check that attributes were parsed correctly.
    assert pytest.approx(spiral.s) == 0.0
    assert pytest.approx(spiral.x) == 100.0
    assert pytest.approx(spiral.y) == 200.0
    assert pytest.approx(spiral.hdg) == 0.5
    assert pytest.approx(spiral.length) == 50.0
    assert pytest.approx(spiral.curv_start) == 0.0
    assert pytest.approx(spiral.curv_end) == 0.02

    # Encode back to XML.
    elem_out = spiral.to_xml()

    # Validate structure and attributes.
    assert elem_out.tag == "geometry"
    assert elem_out.get("s") == "0.0"
    assert elem_out.get("x") == "100.0"
    assert elem_out.get("y") == "200.0"
    assert elem_out.get("hdg") == "0.5"
    assert elem_out.get("length") == "50.0"

    spiral_elem = elem_out.find("spiral")
    assert spiral_elem is not None
    assert spiral_elem.get("curvStart") == "0.0"
    assert spiral_elem.get("curvEnd") == "0.02"

    # Roundtrip check.
    spiral_roundtrip = Spiral.from_xml(elem_out)
    assert spiral == spiral_roundtrip


def test_spiral_missing_spiral_element():
    """Ensure missing <spiral> raises an error."""
    xml_data = """
    <geometry s="0.0" x="0.0" y="0.0" hdg="0.0" length="10.0"/>
    """
    elem = etree.fromstring(xml_data)

    with pytest.raises(AttributeError):
        Spiral.from_xml(elem)
