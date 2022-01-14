import numpy as np

def compute_ankle_costs(mass, gravity, cop_offset, time):
    """
    Compute ankle cost for the AP and ML CoP modulation combined (over time)

    =INPUT=
        mass - float
        gravity - float
        cop_offset_ap - float
        cop_offset_ml - float
        time - array [N,1]

    =OUTPUT=
        required_energy - array [N,1]

    =NOTES=
    
    """

    ankle_moment = mass * gravity * abs(cop_offset)
    required_energy = ankle_moment * time

    return required_energy 