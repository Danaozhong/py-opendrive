from pathlib import Path
from py_opendrive.evaluator.evaluate_opendrive import evaluate_open_drive
from py_opendrive.evaluator.evaluation_properties import EvaluationProperties
from py_opendrive.io.reader import read_file


def test_evaluate_open_drive() -> None:
    # Load an OpenDRIVE file for testing.
    path = Path(r"C:\Work\ODR\sample\test_arc_line.xodr")
    opendrive = read_file(path)

    evaluation_properties = EvaluationProperties(
        shape_points_per_meter=0.3,
    )
    evaluate_open_drive(opendrive, evaluation_properties)
