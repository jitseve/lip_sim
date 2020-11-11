
import numpy as np


class SimulationSettings(object):
    """
    =NOTES=
        t_horizon must be a multiple of t_step
        perturbations are velocity changes
    """

    gravity = 9.81
    t_step = 0.001
    t_horizon = 1
    leg_length = 1
    swing_leg_length = 0.447

    mass_total = 80
    mass_swing_leg = 0.161 * mass_total

    xcom_offset_ap = -0.1364
    xcom_offset_ml = 0.0132

    initial_com_pos_ap = 0
    initial_com_vel_ap = 0.625
    initial_cop_pos_ap = 0
    initial_leg_angle_ap = 0

    initial_com_pos_ml = 0
    initial_com_vel_ml = 0.028
    initial_cop_pos_ml = 0
    initial_leg_angle_ml = 0

    gain_swing_cost_ap = 1
    gain_swing_cost_ml = 1
    gain_sts_cost = 0
    
    perturbations = [9.81 * 0.15 * fraction 
        for fraction in [-0.16, -0.12, -0.08, -0.04, 0.04, 0.08, 0.12, 0.16]]
