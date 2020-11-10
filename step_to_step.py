import numpy as np


def transition_cost(mass, lip_ap, lip_ml, step_pos_ap, step_pos_ml):
    """
    Compute step to step transition cost for the AP and ML directions combined

    =INPUT=
        mass - float
        lip_ap, lip_ml - instance of class LIP2D
        foot_pos_ap, foot_pos_ml - float or ndarray of shape (N,)
    =OUTPUT=
        sts_cost - float or ndarray of shape (N,) or (N, 1)
    =NOTES=
        The vertical component is chosen such that, when it is combined with
        the horizontal components, the resultant velocity vector is perpendicular
        to the leg. Therefore, find a vertical com velocity such that the dot
        product between the leg and the velocity vector is zero.
        The cost is set to infinite for invalid steps, which occurs if the
        foot placement location would be on the same side of the COM as
        the stance foot.
    """

    if isinstance(lip_ap.com_vel, np.ndarray):
        com_vel = np.ones((lip_ap.com_vel.size, 3), dtype='float')
    else:
        com_vel = np.ones((1, 3), dtype='float')
    leg_vector = com_vel.copy()

    # Obtain total velocity vector (note: ones is used above!)
    com_vel[:, 0] = lip_ap.com_vel
    com_vel[:, 1] = lip_ml.com_vel

    # Obtain trailing leg vector
    leg_vector[:, 0], _ = lip_ap.to_local()
    leg_vector[:, 1], _ = lip_ml.to_local()
    leg_vector[:, 2] = lip_ap.leg_length

    # Obtain vertical velocity before transition (should be negative)
    product = leg_vector * com_vel
    pre_vertical_com_vel = (product[:, 0] + product[:, 1]) / -product[:, 2]

    # obtain leading leg vector
    leg_vector[:, 0], _ = lip_ap.to_local(origin=step_pos_ap)
    leg_vector[:, 1], _ = lip_ml.to_local(origin=step_pos_ml)
    
    # Obtain vertical velocity after transition (should be positive)
    product = leg_vector * com_vel
    post_vertical_com_vel = (product[:, 0] + product[:, 1]) / -product[:, 2]
    
    # Compute the step-to-step transition cost (Joule)
    sts_cost = 0.5 * mass * (post_vertical_com_vel - pre_vertical_com_vel)

    # Set sts cost to infinite for invalid steps
    # mask = np.sign(pre_vertical_com_vel) * np.sign(post_vertical_com_vel) >= 0
    # sts_cost[mask] = np.inf
    mask = np.logical_or(
        lip_ap.to_local()[0] * lip_ap.to_local(origin=step_pos_ap)[0] > 0,
        lip_ml.to_local()[0] * lip_ml.to_local(origin=step_pos_ml)[0] > 0)
    sts_cost[mask] = 2**64 - 1

    # Make scalar if input was also scalar
    if not isinstance(lip_ap.com_vel, np.ndarray):
        sts_cost = sts_cost[0]

    return sts_cost

