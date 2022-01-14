"""
Simulation of 2x2D linear inverted pendula, which are linked in time, to
mimic walking motion in a horizontal plane. Step location selection is
according to the XCOM + offset. Step time selection is according to a 
minimization of the step-to-step transition cost and the swing leg cost,
given the XCOM-based stepping location.
"""

import matplotlib
import numpy as np
import time as t
matplotlib.use("TkAgg")
from settings import SimulationSettings
from simulator_v2 import Simulator
from data_plot import DataPlot
from step_analysis import StepAnalysis
from experiment_data_readout import ExperimentReadout as ExpReadout

start_time = t.time()

# Container to store all simulation instances
simulations = []

# Containers to store step data
exp_steps = [[],[]]
model_steps = [[],[]]

# Baseline simulation to steady state gait
simulation = Simulator(SimulationSettings, cop_modulation=SimulationSettings.cop_modulation_steady_state)
simulation.run(n_step=SimulationSettings.n_step_to_steady_state)
data_plot = DataPlot(simulation.sim_data)
(lastvalues, figure_plot, pert_com_pos) = data_plot.plot()
simulations.append(simulation)

# Create plot for full cost landscape
cost_figure = data_plot.cost_plot()

# Set a step that needs to be plot for a step specific cost analysis
stepnr = 1
step_specific_cost_figure = data_plot.step_specific_cost_plot(stepnr)

# Initialise the figures
copfigure = None
stepfigure = None
pertfigure = None

# Save last step of steady-state gait
last_step = [simulation.sim_data.step_pos[1][SimulationSettings.n_step_to_steady_state-1],
            simulation.sim_data.step_pos[0][SimulationSettings.n_step_to_steady_state-1]]

last_com = [simulation.sim_data.com_pos[1][SimulationSettings.n_step_to_steady_state-1],
            simulation.sim_data.com_pos[0][SimulationSettings.n_step_to_steady_state-1]]

# Duplicate the base simulation, then give a different perturbation to each
for pert_idx in range(len(SimulationSettings.perturbations)):
    pert = SimulationSettings.perturbations[pert_idx]
    sim = Simulator(SimulationSettings, cop_modulation=SimulationSettings.cop_modulation_perturbation)
    simulation.copy_state_to(sim)
    data_plot = DataPlot(sim.sim_data)
    
    # Adjust the velocity with the perturbation dependent on chosen perturbation direction in settings
    if SimulationSettings.pertAP is True:
        sim.lip_ap.com_vel += pert
    else:
        sim.lip_ml.com_vel += pert
    
    # Simulate another few steps
    sim.run(n_step=SimulationSettings.n_step_post_perturbation, pert_counter=pert_idx)
    (lastvalues, figure_plot, pert_com_pos) = data_plot.plot(figure=figure_plot, lastvalue=lastvalues, pert_counter=pert_idx)
    
    # Store the simulation
    simulations.append(sim)

    # Take experimental data
    exp_data = ExpReadout()
    (exp_step_pos_y, exp_step_pos_x) = exp_data.com_step_read(pert_counter=pert_idx, perts_com_pos=pert_com_pos, experiment=SimulationSettings.experiment_number)
    exp_steps[1].append(exp_step_pos_y)
    exp_steps[0].append(exp_step_pos_x)

    # Plot experimental data to excisting figure
    exp_data_plot = DataPlot(exp_data)
    exp_data_plot.exp_plot(figure=figure_plot, pert_counter=pert_idx)

    # Create new figure with step data compared to single origin
    (stepfigure, stepx, stepy) = exp_data_plot.step_plot(figure=stepfigure, pert_counter=pert_idx, exp_data=True)
    (stepfigure, stepx, stepy) = data_plot.step_plot(figure=stepfigure, pert_counter=pert_idx, exp_data=False, last_step=last_step)
    if (stepy and stepx) is not None:
        model_steps[0].append(stepx)
        model_steps[1].append(stepy)

    # Create new figure with only the perturbation phase
    pertfigure = data_plot.pert_plot(figure=pertfigure, pert_counter=pert_idx, last_step=last_step, 
                                     last_com=last_com, exp_x=exp_step_pos_x, exp_y=exp_step_pos_y)

    # Plot CoP values for different perturbations
    for event_idx in range(0,4):    #For loop to walk through the different events
        # Take experimental CoP data
        exp_copdata = ExpReadout()
        exp_copdata.cop_read(event=event_idx, plate=SimulationSettings.plate_number, pert_counter=pert_idx, experiment=SimulationSettings.experiment_number)

        # Plot experimental CoP data
        exp_copdata_plot = DataPlot(exp_copdata)
        copfigure = exp_copdata_plot.exp_cop_plot(figure=copfigure, pert_counter=pert_idx, event_counter= event_idx)


# Plot the figures
data_plot.show_plot(figure=figure_plot, x_lim=[-0.15, 0.15], y_lim=[9.15, 10.22], y_label='y', x_label='x',
                    title= 'Linear invertud pendulum walking model')

data_plot.show_plot(figure=pertfigure, x_lim=[-0.14, 0.14], y_lim=[-0.05, 1.03],
                      y_label='AP', x_label='ML', title='Insert Title')
"""
Following plot lines can be used to plot extra data such as cost analysis figures and experimental CoP data

# exp_copdata_plot.show_plot(figure= copfigure, x_lim=[-0.05, 0.3], y_lim=[-0.5, 0.5], y_label='y', x_label='x',
#                             title='Experimental CoP data')

# data_plot.show_plot(figure = step_specific_cost_figure, x_lim=[0,SimulationSettings.t_horizon], y_lim=[0,100], y_label='costs',
#                         x_label='swing time', title='cost posibilities of step {}'.format(stepnr), legend=True)

# data_plot.show_plot(figure = cost_figure, x_lim=[0,SimulationSettings.n_step_to_steady_state], y_lim=[0,10], y_label='costs',
#                         x_label= 'step number', title= 'Cost analysis for full steady state gait', legend=True)

# data_plot.show_plot(figure= stepfigure, x_lim=[-0.3, 0.3], y_lim=[-0.6, 0.6],
#                     y_label='AP', x_label='ML', title='step positions after perturbations')
"""


# Determine correlation matrix
print('-------------- RUN ENDED, ANALYSIS BEGINS --------------')
analysis = StepAnalysis(model_steps, exp_steps, simulation.sim_data.step_pos, simulation.sim_data.time, simulation.sim_data.com_vel)
analysis.compute_analysis_variables()


print("--- %s seconds ---" % (t.time() - start_time))