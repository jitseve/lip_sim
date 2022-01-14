import copy
import numpy as np
from lip2d import LIP2D
from swing_leg import SwingLeg
import step_to_step as STS
import ankle as ANKLE
from data_storage import DataStorage

class Simulator(object):
    """
    Second version of class that handles various simulation steps of the LIP models.
    """

    def __init__(self,settings, cop_modulation=False):
        """
        Set up the simulation environment and its components.
        A time horizon scan is used to determine a future step location and time. 
        A CoP modulating horizon scan is used to determine a future step location and time
        """

        self.settings = settings

        # set time horizon
        self.t_step = settings.t_step
        self.horizon = np.linspace(
            self.t_step, settings.t_horizon, int(settings.t_horizon / self.t_step))

        # set possible CoP offsets
        if cop_modulation is True:
            self.cop_offsets_ap = settings.cop_offsets_ap
            self.cop_offsets_ml = settings.cop_offsets_ml
        else:
            self.cop_offsets_ap = np.array([0])
            self.cop_offsets_ml = np.array([0])

        # create pendula, one for each direction
        self.lip_ap = LIP2D(
            settings.initial_com_pos_ap,
            settings.initial_com_vel_ap,
            settings.initial_foot_pos_ap,
            settings.initial_cop_pos_ap,
            gravity= settings.gravity, leg_length=settings.leg_length)
        self.lip_ml = LIP2D(
            settings.initial_com_pos_ml,
            settings.initial_com_vel_ml,
            settings.initial_foot_pos_ml,
            settings.initial_cop_pos_ml,
            gravity= settings.gravity, leg_length=settings.leg_length)
        
        # set first swing to a right swing
        self.is_right_swing = True

        # create two swing leg pendula
        self.swing_leg_ap = SwingLeg(
            mass=settings.mass_swing_leg,
            gravity=settings.gravity,
            leg_length=settings.swing_leg_length)
        self.swing_leg_ml = SwingLeg(
            mass=settings.mass_swing_leg,
            gravity=settings.gravity,
            leg_length=settings.swing_leg_length)

        # create data storage object
        self.sim_data = DataStorage()

        return


    def run(self, n_step, pert_counter=None):
        """
        Walk for predefined number of steps.
        No perturbations, constant (equivalent) CoP during LIP swing.

        =NOTES=
        This code can be enabled for ML CoP modulation. All 0's for arrays then have to be set to a CoP ml counter
        """

        # Initial swing leg angle
        initial_leg_angle_ap = self.swing_leg_ap.initial_angle
        initial_leg_angle_ml = self.swing_leg_ml.initial_angle
        if initial_leg_angle_ap is None:
            initial_leg_angle_ap = self.settings.initial_leg_angle_ap
        if initial_leg_angle_ml is None:
            initial_leg_angle_ml = self.settings.initial_leg_angle_ml

        for idx_step in range(0, n_step):
            # create various copies of the lips for the possible CoP's
            possible_lips = {'lip_ap': [], 'lip_ml': []}

            for i in range(len(self.cop_offsets_ap)):
                possible_lips['lip_ap'].append(copy.deepcopy(self.lip_ap))
                possible_lips['lip_ap'][i].simulate(self.horizon, self.cop_offsets_ap[i])

            for i in range(len(self.cop_offsets_ml)):
                possible_lips['lip_ml'].append(copy.deepcopy(self.lip_ml))
                possible_lips['lip_ml'][i].simulate(self.horizon, self.cop_offsets_ml[i])
            
            # compute potential new foot positions and their final swing leg angles based on XCoM
            offset_multiplier_ml = {True: 1, False: -1}[self.is_right_swing]
            possible_step_ap = []
            possible_step_ml = []
            possible_final_leg_angle_ap = []
            possible_final_leg_angle_ml = []

            for i in range(len(possible_lips['lip_ap'])):
                possible_step_ap.append(possible_lips['lip_ap'][i].step_location_xcom(
                    offset=self.settings.xcom_offset_ap))
                possible_final_leg_angle_ap.append(possible_lips['lip_ap'][i].to_leg_angle(possible_step_ap[i]))

            for i in range(len(possible_lips['lip_ml'])):
                possible_step_ml.append(possible_lips['lip_ml'][i].step_location_xcom(
                    offset=self.settings.xcom_offset_ml * offset_multiplier_ml))
                possible_final_leg_angle_ml.append(possible_lips['lip_ml'][i].to_leg_angle(possible_step_ml[i]))
            
            # compute swing leg costs
            swing_costs_ap = []
            swing_costs_ml = []

            for i in range(len(possible_lips['lip_ap'])):
                swing_costs_ap.append(self.swing_leg_ap.compute_swing_cost(
                    self.t_step, self.horizon,
                    initial_leg_angle_ap, possible_final_leg_angle_ap[i]))
            
            for i in range(len(possible_lips['lip_ml'])):
                swing_costs_ml.append(self.swing_leg_ml.compute_swing_cost(
                    self.t_step, self.horizon,
                    initial_leg_angle_ml, possible_final_leg_angle_ml[i]))

            # compute step-to-step transition costs
            sts_costs = []

            for i in range(len(self.cop_offsets_ml)):
                sts_costs.append([])
                for j in range(len(self.cop_offsets_ap)):
                    sts_costs[i].append(abs(STS.transition_cost(self.settings.mass_total,
                        possible_lips['lip_ap'][j], possible_lips['lip_ml'][i],
                        possible_step_ap[j], possible_step_ml[i])))

            # compute ankle costs
            # TODO: split into two if you want to gain the anklecosts seperately
            ankle_costs_ap = []
            ankle_costs_ml = []

            for i in range(len(self.cop_offsets_ap)):
                ankle_costs_ap.append(ANKLE.compute_ankle_costs(
                        mass= self.settings.mass_total, gravity=self.settings.gravity,
                        cop_offset=self.cop_offsets_ap[i],
                        time= self.horizon))
            for i in range(len(self.cop_offsets_ml)):
                ankle_costs_ml.append(ANKLE.compute_ankle_costs(
                        mass= self.settings.mass_total, gravity=self.settings.gravity,
                        cop_offset=self.cop_offsets_ml[i],
                        time= self.horizon))
            
            # sum all costs
            total_costs = []
            for i in range(len(swing_costs_ap)):
                total_costs.append(
                    self.settings.gain_swing_cost_ap * swing_costs_ap[i] +
                    self.settings.gain_swing_cost_ml * swing_costs_ml[0] +
                    self.settings.gain_sts_cost * sts_costs[0][i] +
                    self.settings.gain_ankle_cost_ap * ankle_costs_ap[i]+
                    self.settings.gain_ankle_cost_ml * ankle_costs_ml[0]) 

            # == END HORIZON SCAN ==
        
            # Find the lowest costs
            lowest_cost = {'indices': [], 'cost': []}
            for i in range(len(total_costs)):
                lowest_cost['cost'].append(total_costs[i][np.argmin(total_costs[i])])
                lowest_cost['indices'].append(np.argmin(total_costs[i]))
            
            # Best indices that are accompanied with the lowest costs
            best_cop_idx = np.argmin(lowest_cost['cost'])
            best_time_idx = lowest_cost['indices'][best_cop_idx]

            # Use best indices to overwrite lip with best lip model
            self.lip_ap = possible_lips['lip_ap'][best_cop_idx]
            self.lip_ml = possible_lips['lip_ml'][0]

            self.step_pos_ap = possible_step_ap[best_cop_idx]
            self.step_pos_ml = possible_step_ml[0]

            # Take data sample for plotting
            self.sim_data.take_sample(
                self.horizon[best_time_idx],
                self.lip_ap, 
                self.lip_ml,
                self.step_pos_ap[best_time_idx],
                self.step_pos_ml[best_time_idx],
                index= best_time_idx)
            
            # Take cost sample for full gait cost analysis (TODO: enable ml CoP modulation)
            if pert_counter is None:
                self.sim_data.take_fullgait_cost_sample(
                    stepnumber=idx_step,
                    chosen_cop=self.cop_offsets_ap[best_cop_idx],
                    ankle_cost_ap=ankle_costs_ap[best_cop_idx][best_time_idx],
                    ankle_cost_ml=ankle_costs_ml[0][best_time_idx],
                    swing_cost_ap=swing_costs_ap[best_cop_idx][best_time_idx],
                    swing_cost_ml=swing_costs_ml[0][best_time_idx],
                    sts_cost=sts_costs[0][best_cop_idx][best_time_idx]
                )
            
            # Take cost sample for step specific cost analysis
            if pert_counter is None:
                self.sim_data.take_stepspecific_cost_sample(
                    ankle_costs_ap, ankle_costs_ml, swing_costs_ap, swing_costs_ml, sts_costs)

            # Obtain the initial swing leg angle for next step
            initial_leg_angle_ap = self.lip_ap.to_leg_angle()[best_time_idx]
            initial_leg_angle_ml = self.lip_ml.to_leg_angle()[best_time_idx]

            # Update models to new global state
            self.lip_ap.override_state(
                self.lip_ap.com_pos[best_time_idx],
                self.lip_ap.com_vel[best_time_idx],
                self.step_pos_ap[best_time_idx],
                self.step_pos_ap[best_time_idx], cop_shift=0)
            self.lip_ml.override_state(
                self.lip_ml.com_pos[best_time_idx],
                self.lip_ml.com_vel[best_time_idx],
                self.step_pos_ml[best_time_idx],
                self.step_pos_ml[best_time_idx], cop_shift=0)    

            # Change the leg
            self.is_right_swing = not self.is_right_swing

            # Print chosen CoP
            # TODO: is not yet updated for possible ml CoP modulation
            if pert_counter is None:
                print('step', idx_step, 'uses', self.cop_offsets_ap[best_cop_idx], 'as CoP offset')
            else:
                print('perturbation', pert_counter, 'uses', self.cop_offsets_ap[best_cop_idx], 'as CoP offset')

            # if (self.cop_offsets_ap[best_cop_idx] != 0.005263157894736831 and self.cop_offsets_ap[best_cop_idx] != 0):
                # print('ankle is used')

        return   
              
   
    def copy_state_to(self, simulation):

        simulation.lip_ap = copy.deepcopy(self.lip_ap)
        simulation.lip_ml = copy.deepcopy(self.lip_ml)
        simulation.is_right_swing = self.is_right_swing
        simulation.swing_leg_ap = copy.deepcopy(self.swing_leg_ap)
        simulation.swing_leg_ml = copy.deepcopy(self.swing_leg_ml)

        return
