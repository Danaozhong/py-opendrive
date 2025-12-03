from py_opendrive.evaluator.evaluate_road_reference_line import (
    evaluate_segment_road_reference_line,
    SIndexEvaluationProperties,
)
from py_opendrive.evaluator.evaluation_properties import EvaluationProperties
from py_opendrive.geometries.road_reference_line import RoadReferenceLine
import lxml.etree as etree

from py_opendrive.model.header import GeoRef, HeaderOffset


def test_evaluate_road_reference_line() -> None:
    reference_line_xml = """
    <planView>
        <geometry s="0.0000000000000000e+0" x="2.6332314890212541e+2" y="3.0909466577772059e+2" hdg="-1.0293673214774701e-2" length="1.9878307619733022e+1">
            <line/>
        </geometry>
        <geometry s="1.9878307619733022e+1" x="2.8320040338131969e+2" y="3.0889004858859460e+2" hdg="-1.0293673214773813e-2" length="2.8146476527684044e+1">
            <arc curvature="-3.7574482308105735e-2"/>
        </geometry>
        <geometry s="4.8024784147417080e+1" x="3.0624499511718750e+2" y="2.9510498046875000e+2" hdg="-1.0678829575397524e+0" length="3.0418898218134519e+1">
            <arc curvature="-1.6826084264638771e-2"/>
        </geometry>
        <geometry s="7.8443682365551595e+1" x="3.1360132002525052e+2" y="2.6593017830345650e+2" hdg="-1.5797139021955537e+0" length="9.6514329768446032e+0">
            <line/>
        </geometry>
    </planView>
    """
    # Create RoadReferenceLine from the test XML.
    reference_line = RoadReferenceLine.from_xml(etree.fromstring(reference_line_xml))
    assert reference_line is not None

    evaluated_reference_line = evaluate_segment_road_reference_line(
        reference_line,
        EvaluationProperties(
            shape_points_per_meter=5.0,
        ),
        SIndexEvaluationProperties(
            s_start=0.0,
            s_end=reference_line.get_total_length(),
            forced_s_offsets=[],
        ),
        GeoRef(
            offset=HeaderOffset(
                x=10.0,
                y=20.0,
                z=0.0,
                heading=0.01,
            ),
            proj="EPSG:3857",  # Web Mercator projection
        ),
    )
    assert evaluated_reference_line is not None
    # Ensure that the geometry can be exported as a GeoDataFrame.
    evaluated_reference_line.to_file("evaluated_line.gpkg", driver="GPKG")
