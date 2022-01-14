
import numpy as np


class SimulationSettings(object):
    """
    =NOTES=
        ap: antero-posterior
        ml: medio-lateral
        t_horizon must be a multiple of t_step.
        Perturbations are velocity changes.
    """

    # Physical values
    gravity = 9.81
    t_step = 0.001
    t_horizon = 1
    leg_length = 1
    swing_leg_length = 0.447
    body_length = 1.80
    foot_length = 0.21

    mass_total = 80
    mass_swing_leg = 0.161 * mass_total

    # Set possible CoP shifts
    cop_ap_minimal = -0.05
    cop_steps = 6
    cop_offsets_ap = np.linspace(
            cop_ap_minimal, cop_ap_minimal + foot_length, cop_steps)
    cop_offsets_ml = np.array([0]) # CoP shift in ML direction is not included

    # XCoM offsets
    xcom_offset_ap = -0.1364
    xcom_offset_ml = 0.0132

    # Initial conditions for the LIPs
    initial_com_pos_ap = 0
    initial_com_vel_ap = 0.625
    initial_cop_pos_ap = 0
    initial_foot_pos_ap = 0
    initial_leg_angle_ap = 0

    initial_com_pos_ml = 0
    initial_com_vel_ml = 0.028
    initial_cop_pos_ml = 0
    initial_foot_pos_ml = 0
    initial_leg_angle_ml = 0

    # Chosen cost gains
    gain_swing_cost_ap = 1
    gain_swing_cost_ml = 1
    gain_sts_cost = 0.1
    gain_ankle_cost_ap = 0.33
    gain_ankle_cost_ml = 1

    print('The chosen gains are:', '\nSwing ap:', gain_swing_cost_ap, '\nSwing ml:', gain_swing_cost_ml,
        '\nSTS:', gain_sts_cost, '\nAnkle ap:', gain_ankle_cost_ap, '\nAnkle ml', gain_ankle_cost_ml)

    # Amount of steps performed by the model
    n_step_to_steady_state = 20     # steps before perturbation
    n_step_post_perturbation = 1    # steps after perturbation

    # Set CoP modulation for two model phases
    cop_modulation_steady_state = False
    cop_modulation_perturbation = True

    # Choose perturbation direction (ML/AP)
    pertAP = True

    if pertAP is False:
        experiment_number = 0
    elif pertAP is True:
        experiment_number = 2

    plate_number = 0

    # Set perturbation magnitudes
    perturbations = [9.81 * 0.15 * fraction 
        for fraction in [-0.04, -0.08, -0.12, -0.16, 0.04, 0.08, 0.12, 0.16]]
