import numpy as np
import math as m

class StepAnalysis(object):

    def __init__(self, model_steps, experiment_steps, ss_step_positions, ss_swingtimes, ss_com_vel):
        self.model_steps = model_steps
        self.experiment_steps = [experiment_steps[1], experiment_steps[0]]
        self.ss_step_positions = ss_step_positions
        self.ss_swingtimes = ss_swingtimes
        self.ss_com_vel = ss_com_vel

        return

    def compute_analysis_variables(self):
        # Compute correlation matrix and r^2 values
        corr_matrix_y = np.corrcoef(self.experiment_steps[0], self.model_steps[0])
        corr_matrix_x = np.corrcoef(self.experiment_steps[1], self.model_steps[1])
        r2_matrix_x = np.square(corr_matrix_x)
        r2_matrix_y = np.square(corr_matrix_y)

        print('\nr-squared ML is: ',r2_matrix_x[0][1])
        print('r-squared AP is: ',r2_matrix_y[0][1])

        # Compute distance array
        dist_x = abs(np.subtract(self.experiment_steps[0],self.model_steps[0]))
        dist_y = abs(np.subtract(self.experiment_steps[1],self.model_steps[1]))

        dist = np.sqrt(np.add(np.square(dist_x),np.square(dist_y)))

        # Compute root mean square of all individual distances
        summation = 0
        for idx in range(len(dist)):
            summation += dist[idx] ** 2
        
        RMS = m.sqrt((1/len(dist))*summation)

        print('\nRMS of distances is: ', RMS)

        # Compute average step length
        steplengths = [x - self.ss_step_positions[0][i - 1] for i, x in enumerate(self.ss_step_positions[0]) if i > 0]
        mean_steplength = np.mean(steplengths)
        print('\nThe average steplength during steady state gate is: ', mean_steplength)

        # Compute average step width
        stepwidths = np.abs([x - self.ss_step_positions[1][i - 1] for i, x in enumerate(self.ss_step_positions[1]) if i > 0])
        mean_stepwidth = np.mean(stepwidths)
        print('The average step width during steady state gate is: ', mean_stepwidth)

        # Compute average swing time
        mean_steptime = np.mean(self.ss_swingtimes)
        print('The average swing time is: ', mean_steptime)

        # Compute average forward velocity
        mean_velocity = np.mean(self.ss_com_vel[0])
        print('The average forward velocity is: ', mean_velocity, '\n')

        return RMS

