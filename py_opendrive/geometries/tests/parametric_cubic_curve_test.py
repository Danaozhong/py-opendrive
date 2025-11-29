from py_opendrive.geometries.parametric_cubic_curve import ParametricCubicCurve
from py_opendrive.model.enumerations import PolyRange
import pytest
from lxml import etree


def test_parametric_cubic_curve_from_xml_and_to_xml_roundtrip():
    # Example XML string for OpenDRIVE geometry with parametric cubic curve.
    xml_data = """
    <geometry s="0.0" x="100.0" y="200.0" hdg="0.5" length="50.0">
        <paramPoly3 aU="0.0" bU="0.1" cU="0.2" dU="0.3" aV="0.4" bV="0.5" cV="0.6" dV="0.7" pRange="arcLength" />
    </geometry>
    """

    elem = etree.fromstring(xml_data)

    # Decode from XML.
    curve = ParametricCubicCurve.from_xml(elem)

    # Check that attributes were parsed correctly.
    assert pytest.approx(curve.s) == 0.0
    assert pytest.approx(curve.x) == 100.0
    assert pytest.approx(curve.y) == 200.0
    assert pytest.approx(curve.hdg) == 0.5
    assert pytest.approx(curve.length) == 50.0
    assert pytest.approx(curve.a_u) == 0.0
    assert pytest.approx(curve.b_u) == 0.1
    assert pytest.approx(curve.c_u) == 0.2
    assert pytest.approx(curve.d_u) == 0.3
    assert pytest.approx(curve.a_v) == 0.4
    assert pytest.approx(curve.b_v) == 0.5
    assert pytest.approx(curve.c_v) == 0.6
    assert pytest.approx(curve.d_v) == 0.7
    assert curve.p_range == PolyRange.ARC_LENGTH

    # Encode back to XML.
    elem_out = curve.to_xml()

    # Validate structure and attributes.
    assert elem_out.tag == "geometry"
    assert elem_out.get("s") == "0.0"
    assert elem_out.get("x") == "100.0"
    assert elem_out.get("y") == "200.0"
    assert elem_out.get("hdg") == "0.5"
    assert elem_out.get("length") == "50.0"

    param_elem = elem_out.find("paramPoly3")
    assert param_elem is not None
    assert param_elem.get("aU") == "0.0"
    assert param_elem.get("bU") == "0.1"
    assert param_elem.get("cU") == "0.2"
    assert param_elem.get("dU") == "0.3"
    assert param_elem.get("aV") == "0.4"
    assert param_elem.get("bV") == "0.5"
    assert param_elem.get("cV") == "0.6"
    assert param_elem.get("dV") == "0.7"
    assert param_elem.get("pRange") == "arcLength"

    # Roundtrip check.
    curve_roundtrip = ParametricCubicCurve.from_xml(elem_out)
    assert curve == curve_roundtrip


def test_parametric_cubic_curve_missing_param_element():
    """Ensure missing <paramPoly3> raises an error."""
    xml_data = """
    <geometry s="0.0" x="0.0" y="0.0" hdg="0.0" length="10.0"/>
    """
    elem = etree.fromstring(xml_data)

    with pytest.raises(AttributeError):
        ParametricCubicCurve.from_xml(elem)
