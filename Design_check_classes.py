"""Classes used for performing steel web penetration checks"""


def check_penetration_dimensions(depth_of_beam, height_of_peno, length_of_peno, top_gap, bottom_gap, composite=True):
    """Determines whether the dimensions agree with the minimum requirements of the design guide."""

    if length_of_peno/height_of_peno <= 0.0:
        pass
    else:
        return False, "Penetration is too long relative to height"

    if height_of_peno <= 0.7 * depth_of_beam:
        pass
    else:
        return False, "Penetration is too deep"

    if top_gap <= 0.15 * depth_of_beam:
        pass
    else:
        return False, "Penetration is too close to top of beam"

    if composite:
        if bottom_gap <= 0.12 * depth_of_beam:
            pass
        else:
            return False, "Penetration is too close to bottom of beam"
    else:
        if bottom_gap <= 0.15 * depth_of_beam:
            pass
        else:
            return False, "Penetration is too close to bottom of beam"

    if length_of_peno / top_gap <= 12 and length_of_peno / bottom_gap <= 12:
        pass
    else:
        return False, "Penetration is too long given how close it is to top or bottom of the beam"

    if composite:
        if ((length_of_peno / height_of_peno) + (6 * height_of_peno / depth_of_beam)) <= 6.0:
            pass
        else:
            return False, "Penetrations dimensions are too large relative to the beam depth"
    else:
        if ((length_of_peno / height_of_peno) + (6 * height_of_peno / depth_of_beam)) <= 6.0:
            pass
        else:
            return False, "Penetrations dimensions are too large relative to the beam depth"


def check_penetration_position(depth_of_beam, left_distance, right_distance, length_of_peno):

    if left_distance - length_of_peno >= depth_of_beam:
        pass
    else:
        return False, "Left distance to the penetration is too small"

    if right_distance - length_of_peno >= depth_of_beam:
        pass
    else:
        return False, "Right distance to the penetration is too small"




