
class DataStorage(object):
    """
    Class to keep track of simulation data.

    """

    def __init__(self):
        self.time = []
        self.com_pos = [[], []]
        self.com_vel = [[], []]
        self.cop_pos = [[], []]
        self.xcom_pos = [[], []]
        self.step_pos = [[], []]
       
        self.cost_landscape_specificstep = {'ankle_cost_ap': [], 'ankle_cost_ml': [], 'swing_cost_ap': [], 'swing_cost_ml': [], 'sts_cost': []}

        self.cost_landscape_fullgait = {'step_number': [], 'chosen_cop': [], 'ankle_cost_ap': [], 'ankle_cost_ml': [], 'swing_cost_ap': [], 'swing_cost_ml': [], 'sts_cost': []}
        return

    
    def take_sample(self, time, lip_ap, lip_ml, step_pos_ap, step_pos_ml, index=None):
        com_pos_ap, com_vel_ap, cop_origin_ap, cop_pos_ap, cop_shift_ap, xcom_pos_ap = lip_ap.state_at(index)
        com_pos_ml, com_vel_ml, cop_origin_ml, cop_pos_ml, cop_shift_ml, xcom_pos_ml = lip_ml.state_at(index)
        
        self.time.append(time)
        
        self.com_pos[0].append(com_pos_ap)
        self.com_vel[0].append(com_vel_ap)
        self.cop_pos[0].append(cop_origin_ap + cop_shift_ap)
        self.xcom_pos[0].append(xcom_pos_ap)
        self.step_pos[0].append(step_pos_ap)

        self.com_pos[1].append(com_pos_ml)
        self.com_vel[1].append(com_vel_ml)
        self.cop_pos[1].append(cop_origin_ml + cop_shift_ml)
        self.xcom_pos[1].append(xcom_pos_ml)
        self.step_pos[1].append(step_pos_ml)
        return

    def take_stepspecific_cost_sample(self, ankle_cost_ap, ankle_cost_ml, swing_cost_ap, swing_cost_ml, sts_cost):
        self.cost_landscape_specificstep['ankle_cost_ap'].append(ankle_cost_ap)
        self.cost_landscape_specificstep['ankle_cost_ml'].append(ankle_cost_ml)
        self.cost_landscape_specificstep['swing_cost_ap'].append(swing_cost_ap)
        self.cost_landscape_specificstep['swing_cost_ml'].append(swing_cost_ml)
        self.cost_landscape_specificstep['sts_cost'].append(sts_cost)
        return


    def take_fullgait_cost_sample(self, stepnumber, chosen_cop, ankle_cost_ap, ankle_cost_ml, swing_cost_ap, swing_cost_ml, sts_cost ):
        self.cost_landscape_fullgait['step_number'].append(stepnumber)
        self.cost_landscape_fullgait['chosen_cop'].append(chosen_cop)
        self.cost_landscape_fullgait['ankle_cost_ap'].append(ankle_cost_ap)
        self.cost_landscape_fullgait['ankle_cost_ml'].append(ankle_cost_ml)
        self.cost_landscape_fullgait['swing_cost_ap'].append(swing_cost_ap)
        self.cost_landscape_fullgait['swing_cost_ml'].append(swing_cost_ml)
        self.cost_landscape_fullgait['sts_cost'].append(sts_cost)
        return