"""
Simulation of 2x2D linear inverted pendula, which are linked in time, to
mimic walking motion in a horizontal plane. Step location selection is
according to the XCOM + offset. Step time selection is according to a 
minimization of the step-to-step transition cost and the swing leg cost,
given the XCOM-based stepping location.
"""


from settings import SimulationSettings
from simulator import Simulator


# Container to store all simulation instances
simulations = []

# Baseline simulation to steady state gait
simulation = Simulator(SimulationSettings)
simulation.run(n_step=SimulationSettings.n_step_to_steady_state)
simulation.sim_data.plot()
simulations.append(simulation)


# Duplicate the base simulation, then give a different perturbation to each
for pert in SimulationSettings.perturbations:
    sim = Simulator(SimulationSettings)
    simulation.copy_state_to(sim)
    
    # Adjust the lateral velocity with the perturbation
    sim.lip_ml.com_vel += pert
    
    # Simulate another few steps
    sim.run(n_step=SimulationSettings.n_step_post_perturbation)
    sim.sim_data.plot(append_axis=simulation.sim_data.figure.axes[0])
    
    # Store the simulation
    simulations.append(sim)


simulation.sim_data.show_plot()
# simulation.sim_data.figure.axes[0].set_ylim([18.5, 20])

