import constants


def anchor_interval_to_octave_and_representative_string(anchor_interval) -> str:
    octave, representative = divmod(anchor_interval, constants.NUM_NOTES)
    return str(representative) + str(("'" if octave >= 0 else ",") * abs(octave))

def get_anchor_interval_representative(anchor_interval) -> int:
    return anchor_interval % 12