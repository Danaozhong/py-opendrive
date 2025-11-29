from py_opendrive.io.reader import read_file
from py_opendrive.io.writer import write_file
import tempfile
from pathlib import Path


def test_round_trip():
    """Tests reading and writing of sample OpenDRIVE files."""

    # Test the ODR files provided by the OpenDRIVE project
    current_dir = Path(__file__).parent
    input_files = [
        current_dir / "sample_data/Town04.xodr",
        current_dir / "sample_data/Town05.xodr",
    ]

    for input_file in input_files:
        open_drive = read_file(input_file)
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_file = Path(tmpdirname) / input_file.name
            write_file(open_drive, output_file)

            # Read back the written file
            open_drive_round_trip = read_file(output_file)

            # Assert that the original and round-trip instances are equal
            assert open_drive == open_drive_round_trip
