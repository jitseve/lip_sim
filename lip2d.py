
import numpy as np


class LIP2D(object):

    def __init__(self, com_pos, com_vel, cop_pos=0, gravity=9.81, leg_length=1):
        """
        =INPUT=
            com_pos - float or ndArray
            com_vel - float or ndArray
                Initial center of mass position and velocity. 
                If ndArray, most be of same dimensions.
            cop_pos - float
                Initial center of pressure velocity
                If ndArray, must be of same dimensions as com_pos and com_vel
            gravity - float [9.81]
                Gravitational constant
            leg_length - float [1]
        """

        # Model properties
        self.leg_length = leg_length
        self.w0 = np.sqrt(gravity / leg_length)

        # Model state
        self.com_pos = com_pos
        self.com_vel = com_vel
        self.cop_pos = cop_pos

        return


    def simulate(self, t_step):
        """
        =INPUT=
            t_step - float
                Time step to simulate over.
                If negative, provide backward-time solution.
        """

        com_pos_new = (self.cop_pos
            + (self.com_pos - self.cop_pos) * np.cosh(self.w0 * t_step)
            + self.com_vel / self.w0 * np.sinh(self.w0 * t_step))

        com_vel_new = (
            (self.com_pos + self.cop_pos) * self.w0 * np.sinh(self.w0 * t_step)
            + self.com_vel * np.cosh(self.w0 * t_step))

        self.com_pos = com_pos_new
        self.com_vel = com_vel_new

        return
    