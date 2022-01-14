import scipy.io as sio

class ExperimentReadout(object):
    """
    Class to read and store the experimental data.

    """

    def __init__(self):
        self.time = []
        self.com_pos = [[], []]
        self.com_vel = [[], []]
        self.cop_pos = [[], []]
        self.step_pos = [[], []]
        self.exp_step_pos = [[],[]]

        return


    def com_step_read(self, pert_counter, perts_com_pos, experiment=0):
        """
        Function that reads the mean com and step locations gathered from experiments (Vlutters et al, 2017).

        =INPUT=
            pert_counter: decides which perturbation value needs to be read
            perts_com_pos: position of the COM of the current perturbation
            experiment: decides from which experiment the value's will be read
        """
        # Use Scipy to load the data
        # Note: Pathing must be changed to where you have stored the experimental data locally
        com_mean_perturbation = sio.loadmat('/home/jitseve/Documents/bacheloropdracht/Exp_Data_2/com_mean_perturbation.mat')

        # Get the numpy array from the created dictionary
        com_mean_perturbation = com_mean_perturbation['comDatape_m2']
      
        # Read model CoM location
        self.com_pos[0].append(perts_com_pos[0])           # X-coordinates 
        self.com_pos[1].append(perts_com_pos[1])           # Y-coordinates

        # Take step location (CoM right foot)
        step_posx = perts_com_pos[0] + com_mean_perturbation[2, 6, 0, pert_counter, experiment]
        step_posy = perts_com_pos[1] + com_mean_perturbation[2, 6, 1, pert_counter, experiment]
        self.step_pos[0].append(step_posx)
        self.step_pos[1].append(step_posy)

        # Take original step location
        self.exp_step_pos[0].append(com_mean_perturbation[2, 6, 0, pert_counter, experiment])  
        self.exp_step_pos[1].append(com_mean_perturbation[2, 6, 1, pert_counter, experiment]) 

        compensated_step_posx= com_mean_perturbation[2, 6, 0, pert_counter, experiment]
        compensated_step_posy= com_mean_perturbation[2, 6, 1, pert_counter, experiment]

        return step_posy, step_posx


    def cop_read(self, event=0, plate=0, pert_counter=0, experiment=0):
        """
        Function that reads the mean cop data from experiments (Vlutters et al, 2017)

        =INPUT=
        event: decides from which event the CoP data needs to be read
        plate: decides from which plate the CoP data needs to be read (1=right plate, 2=left plate, 3=both plates)
        pert_counter: decides which perturbation value needs to be read
        experiment: decide from which experiment values need to be read 
        """
        # Use Scipy to load the data
        cop_mean_perturbation = sio.loadmat('/home/jitseve/Documents/bacheloropdracht/Exp_Data_2/cop_mean_perturbation.mat')

        # Get the numpy array
        cop_mean_perturbation = cop_mean_perturbation['copDatape_m2']

        # Save the x and y data in self
        cop_xlocation = cop_mean_perturbation[event, plate*2, pert_counter, experiment]
        cop_ylocation = cop_mean_perturbation[event, plate*2+1, pert_counter, experiment]
        self.cop_pos[0].append(cop_xlocation)
        self.cop_pos[1].append(cop_ylocation)

        return