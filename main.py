
from settings import SimulationSettings
from simulator import Simulator


# TODO: error in swing leg cost?

# Container to store all simulation instances
simulations = []

# Baseline simulation to steady state gait
simulation = Simulator(SimulationSettings)
simulation.run(n_step=10)
simulation.sim_data.plot()
simulations.append(simulation)

# simulation.sim_data.show_plot()



# Duplicate the base simulation, then give a different perturbation to each
# for pert in SimulationSettings.perturbations:
#     sim = Simulator(SimulationSettings)
#     simulation.copy_state_to(sim)
    
#     # Adjust the lateral velocity with the perturbation
#     sim.lip_ml.com_vel += pert
    
#     # Simulate another few steps
#     sim.run(n_step=1)
#     sim.sim_data.plot(append_axis=simulation.sim_data.figure.axes[0])
#     # Store the simulation
#     simulations.append(sim)



# simulation.sim_data.show_plot()
# simulation.sim_data.figure.axes[0].set_ylim([18.5, 20])

