
import numpy as np


class SwingLeg(object):
    """
    Swing leg swings following half of a cosine wave, such that the initial
    and final velocity are 0.
    """

    def __init__(self, mass, gravity=9.81, leg_length=0.447):
        """
        =INPUT=
            mass - float
            gravity - float [9.81]
            leg_length - float [0.447]
                Default value is based on Winter, 2009, for distance swing leg
                mass from hip joint, assuming a straight knee.
        """
        # Simulation properties
        self.gravity = gravity

        # Leg properties
        self.mass = mass
        self.leg_length = leg_length

        # Leg swing properties
        self.initial_angle = None
        self.final_angle = None
        self.wave_frequency = None
        self.wave_amplitude = None
        return


    def compute_swing_cost(self, t_step, t_swing, initial_angle, final_angle):
        """
        Compute swing cost from initial to final leg angle over t_swing seconds.
        =INPUT=
            t_step - float
                Time step used in computing moment profiles
            t_swing - float or ndarray of shape (N,) or (N, 1)
                Total swing time between initial and final leg angle
            initial_angle - float or ndarray of shape (N,) or (N, 1)
            final_angle - float or ndarray of shape (N,) or (N, 1)
                Swing leg initial and final angle
        =OUTPUT=
            swing_cost - float or ndarray of shape (N,) or (N, 1)
        =NOTES=
            If t_swing is an array, there can be various final swing times.
            A different horizon could be created for each of them, to compute
            the moment profile up to that t_swing. However, only 1 horizon
            array gets created, up to the longest t_swing, and evaluated
            for all points. This means that the horizon exceeds most t_swing.
            This is  computationally more efficient (no python loops).
        """

        # Check dimensions
        is_dimension_adjusted = [False, False, False]
        if isinstance(t_swing, np.ndarray) and len(t_swing.shape) == 1:
            t_swing.shape = (-1, 1)
            is_dimension_adjusted[0] = True
        if isinstance(t_swing, np.ndarray) and len(initial_angle.shape) == 1:
            initial_angle.shape = (-1, 1)
            is_dimension_adjusted[1] = True
        if isinstance(t_swing, np.ndarray) and len(final_angle.shape) == 1:
            final_angle.shape = (-1, 1)
            is_dimension_adjusted[2] = True

        # Configure the swing leg
        self.initial_angle = initial_angle
        self.final_angle = final_angle
        self.set_frequency(t_swing)
        self.set_amplitude()
        
        # Create a grid of evaluation points for moment profile
        if isinstance(t_swing, np.ndarray):
            t_swing_max = t_swing.max()
        else:
            t_swing_max = t_swing
        t_leg = np.linspace(t_step, t_swing_max, int(t_swing_max / t_step))
        t_leg.shape = (1, -1)
        
        # Obtain moment profile
        moment_profile = self.leg_moment_profile(t_leg)
        
        # Compute the cost
        # TODO: the diag gives problems if not square...
        swing_cost = np.cumsum(abs(moment_profile) * t_step, axis=1).diagonal()
        swing_cost.shape = (-1,)

        # Revert to original dimensions
        if is_dimension_adjusted[0]:
            t_swing.shape = (-1,)
        if is_dimension_adjusted[1]:
            initial_angle.shape = (-1,)
        if is_dimension_adjusted[2]:
            final_angle.shape = (-1,)

        return swing_cost


    def set_frequency(self, t_swing):
        """
        =INPUT=
            t_swing - float or ndarray
                Total swing duration
        """
        self.wave_frequency = 1 / (2 * t_swing)
        return


    def set_amplitude(self):
        self.wave_amplitude = self.final_angle - self.initial_angle / 2
        return


    def leg_moment_profile(self, t_leg):
        """
        Obtain the hip moment exerted at the swing leg at t_leg,
        where 0 <= t_leg <= t_swing, following equations of motion for
        a hanging pendulum.
        
        =INPUT=
            t_leg - float or ndarray of shape (1, N)
                Where N is the number of time instances to evaluate at
        """
        return (self.mass * self.leg_length**2 * 
            self.leg_acceleration_profile(t_leg) +
            self.mass * self.gravity * self.leg_length *
            np.sin(self.leg_angle_profile(t_leg)))


    def leg_angle_profile(self, t_leg):
        """
        Obtain the leg angle at t_leg, where 0 <= t_leg <= t_swing

        =INPUT=
            t_leg - float or ndarray of shape (1, N)
                Where N is the number of time instances to evaluate at
        =OUTPUT=
            Leg angle evaluated at t_leg. of the same dimensions as t_leg.
        """
        return (self.initial_angle + self.wave_amplitude - self.wave_amplitude 
            * np.cos(2 * np.pi * self.wave_frequency * t_leg))

    
    def leg_velocity_profile(self, t_leg):
        """
        See leg_angle_profile
        """
        return (self.wave_amplitude * 2 * np.pi * self.wave_frequency * np.sin(
            2 * np.pi * self.wave_frequency * t_leg))
        

    def leg_acceleration_profile(self, t_leg):
        """
        See leg_angle_profile
        """
        return (self.wave_amplitude * (2 * np.pi * self.wave_frequency)**2 
        * np.cos(2 * np.pi * self.wave_frequency * t_leg))
