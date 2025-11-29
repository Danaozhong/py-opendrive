def calculate_geometry_evaluation_points():
    """Calculates at which points the OpenDRIVE geometries need to be evaluated.
    There are several criteria for this:
    1) Whenever there is an attribute change at a certain s position, this geometry must be evaluated.
    2) Depending on the evaluation properties (e.g. shape points per meter), additional points may be needed.
    """

    # TODO get a list of all s values, where attributes in the map are changing.
    s_points = [0.0, 1.0]

    print(s_points)
    # Apply the geometry interpolation.
    # s_points = interpolate_geometries(s_points)

    # TODO implementation.
