
from settings import SimulationSettings
from simulator import Simulator


simulation = Simulator(SimulationSettings)
simulation.run(n_step=10)

simulation.sim_data.plot()
