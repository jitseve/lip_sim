
import numpy as np


class LIP2D(object):

    def __init__(self, com_pos, com_vel, cop_pos=0, gravity=9.81, leg_length=1):
        """
        Two-dimensional linear inverted pendulum (LIP)

        =INPUT=
            com_pos - float or ndarray of shape (N,) or (N, 1)
            com_vel - float or ndarray of shape (N,) or (N, 1)
                Initial center of mass position and velocity. 
                If ndarray, most be of same dimensions.
            cop_pos - float or ndarray of shape (N,) or (N, 1)
                Initial center of pressure velocity
                If ndarray, must be of same dimensions as com_pos and com_vel
            gravity - float [9.81]
                Gravitational constant
            leg_length - float [1]
        =NOTES=
            Because the pendulum is linear, the leg_length is actually the
            constant height of the COM. The leg itself is telescopic: it needs
            to increase in length if the COM moves away from upright.
        """

        # Model properties
        self.leg_length = leg_length
        self.w0 = np.sqrt(gravity / leg_length)

        # Model state (global)
        self.com_pos = com_pos
        self.com_vel = com_vel
        self.cop_pos = cop_pos
        self.xcom_pos = self.to_xcom()
        self.leg_angle = self.to_leg_angle()
        
        return


    def simulate(self, t_step):
        """
        Simulate the LIP using its equations of motion. For as long as
        cop_pos remains constant, the state at any future or past time
        can be obtained.

        =INPUT=
            t_step - float or ndarray of shape (N,) or (N, 1)
                Time step(s) to simulate over.                
                If ndarray, com_pos, com_vel, and xcom_pos will take
                the same dimensions.
        """

        com_pos_new = (self.cop_pos
            + (self.com_pos - self.cop_pos) * np.cosh(self.w0 * t_step)
            + self.com_vel / self.w0 * np.sinh(self.w0 * t_step))

        com_vel_new = (
            (self.com_pos - self.cop_pos) * self.w0 * np.sinh(self.w0 * t_step)
            + self.com_vel * np.cosh(self.w0 * t_step))

        self.override_state(com_pos_new, com_vel_new, self.cop_pos)

        return
    

    def to_xcom(self):
        """
        Compute and return the XCOM position
        """
        return self.com_pos + self.com_vel / self.w0


    def to_leg_angle(self, foot_position=None):
        """
        Compute leg angle with the vertical using the model's constant height.

        =INPUT= 
            foot_position - float or ndarray of shape (N,) or (N, 1) [None]
                Global point-foot position. If None, current COP is used.
        =OUTPUT=
            leg_angle - float or ndarray
                In radian. Will have the same dimensions as com_pos.
        =NOTES=
            Counter-clockwise is positive.
        """
        if foot_position is None:
            foot_position = self.cop_pos

        return np.arctan((foot_position - self.com_pos) / self.leg_length)


    def to_local(self, origin=None):
        """
        Make model position parameters relative to some origin.

        =INPUT=
            origin - float or ndarray of shape (N,) or (N, 1) [None]
                If not provided, the model's COP is used as origin.
        =OUTPUT=
            com_pos - float or ndarray of shape (N,) or (N, 1)
                Relative to selected origin
            xcom_pos - float or ndarray of shape (N,) or (N, 1)
                Relative to selected origin
        """
        if origin is None:
            return (self.com_pos - self.cop_pos, self.xcom_pos - self.cop_pos)
        else:
            return (self.com_pos - origin, self.xcom_pos - origin)


    def step_location_xcom(self, offset=0):
        """
        Compute XCOM-offset-based stepping location.

        =INPUT=
            offset - float [0]
                Offset from the XCOM to compute a step location with
        =OUTPUT=
            step_location - float or ndarray of shape (N,) or (N, 1)
                Constant offset control based stepping location.
                Is an array if xcom_pos is also an array.
        """
        return self.xcom_pos + offset


    def override_state(self, com_pos, com_vel, cop_pos):
        """
        =INPUT=
            See __init__
        =NOTES=
            leg_angle_pre_step can function as initial swing leg angle
            for the motion post-step
        """
        self.com_pos = com_pos
        self.com_vel = com_vel
        self.cop_pos = cop_pos
        self.xcom_pos = self.to_xcom()
        self.leg_angle = self.to_leg_angle()
        return


    def state_at(self, index=None):
        """
        Retrieve state at certain index if state is an ndarray.
        TODO: doesn't work yet if cop_pos is an array...
        """
        if index is not None:
            return (self.com_pos[index], self.com_vel[index], self.cop_pos, self.xcom_pos[index])
        else:
            return (self.com_pos, self.com_vel, self.cop_pos, self.xcom_pos)

        