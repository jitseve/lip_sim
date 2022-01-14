from matplotlib import pyplot as plt
from settings import SimulationSettings
import numpy as np
import math as m

class DataPlot(object):
    """
    Class to plot the simulation data stored in DataStorage
    """

    def __init__(self, storeddata):
        """
        Data plotter

        =INPUT=
            storeddata - Data container containing:
                            - CoM positions
                            - CoP positions
                            - Step positions
                            - Time data
        
        =NOTES=
            Because we initialize this class twice (for the baseline model and for the perturbations)
            the figure is not initialised in the self container. If we would we could not re-use the same figure 
            for the second initialisation
        """
        self.storage = storeddata
                    
        self.com_pos = storeddata.com_pos
        self.cop_pos = storeddata.cop_pos
        self.step_pos = storeddata.step_pos

        self.colors = (  (0, 0, 0.99608), (0, 0.50196, 0.99608), (0, 0.99608, 0.99608),
                    (0.50196, 0.99608, 0.50196), (0.99608, 0.99608, 0), (0.99608, 0.50196, 0), 
                    (0.99608, 0, 0), (0.50196, 0, 0) )

        self.markers = ( 'o' , 'v' , ' x' , '+' , 'x', 'd' )
        return


    def plot(self, figure=None , lastvalue=None, pert_counter=None):
        """
        =INPUT=
        figure: 
            is none for plotting of baseline simulation and the excisting figure for perturbation simulation
        lastvalue: 
            is none for plotting of baseline simulation and position of last CoM of baseline simulation for perturbation simulation
        pert_counter:
            is none for plotting of baseline simulation and number of the perturbation for the perturbation simulation 
        
        =OUTPUT=
        lastvalue:
            is the position of the last CoM of the baseline simulation
        figure:
            keeps the current figure
        perts_com_pos:
            The com position of the current perturbation
        
        =NOTES=
        Colors under the assumption that first stance leg is left;
        Left: blue
        Right: red
        CoM: black
        Walking path: black dashed line

        The colors of the perturbations are for the different perturbations
        """

        if figure is None:
            figure = plt.figure(0)
            ax = figure.add_subplot(1, 1, 1)

        else:
            ax = figure.axes[0]

        # COM position
        if pert_counter is None:
            ax.plot(self.com_pos[1], self.com_pos[0], 'ok', markersize=10, label= 'CoM positions')
        else:
            ax.plot(self.com_pos[1], self.com_pos[0], 'ok', markersize=10)


        # Walking path
        if lastvalue is None:
            x_val = self.com_pos[1]
            y_val = self.com_pos[0]
            lastvalue = (x_val[-1], y_val[-1])
            perts_com_pos = None

        else:
            x_val = (lastvalue[0], self.com_pos[1][0])
            y_val = (lastvalue[1], self.com_pos[0][0])
            perts_com_pos = (self.com_pos[1][0], self.com_pos[0][0])

        ax.plot(x_val, y_val, '--k')

        # Foot positions
        if pert_counter is None:
            ax.plot(self.step_pos[1][1::2], self.step_pos[0][1::2], '^',
                markersize=8, markerfacecolor=(1, 1, 1, 0), markeredgecolor='b', label= 'foot position left')
            ax.plot(self.step_pos[1][0::2], self.step_pos[0][0::2], '^',
                markersize=8, markerfacecolor=(1, 1, 1, 0), markeredgecolor='r', label='foot position right')
        else:
            ax.plot(self.step_pos[1], self.step_pos[0], '^',
                markersize=8 , markerfacecolor=(1, 1, 1, 0), markeredgewidth=3, markeredgecolor=self.colors[pert_counter])

        # CoP locations
        if pert_counter is None:
            ax.plot(self.cop_pos[1][0], self.cop_pos[0][0], '+',
                markersize=8, markerfacecolor=(1, 1, 1, 0), markeredgecolor='k', label= 'Initial CoP position')
            self.cop_pos[0].pop(0)
            self.cop_pos[1].pop(0)
            ax.plot(self.cop_pos[1][1::2], self.cop_pos[0][1::2], '+',
                markersize=8, markerfacecolor=(1, 1, 1, 0), markeredgecolor='b', label= 'CoP position left')
            ax.plot(self.cop_pos[1][0::2], self.cop_pos[0][0::2], '+',
                markersize=8, markerfacecolor=(1, 1, 1, 0), markeredgecolor='r', label= 'CoP position right')
        else:
            ax.plot(self.cop_pos[1], self.cop_pos[0], '+',
                markersize=8 , markerfacecolor=(1, 1, 1, 0), markeredgewidth=3, markeredgecolor=self.colors[pert_counter])


        # XCOM position
        # ax.plot(self.xcom_pos[1], self.xcom_pos[0], 'xm')  

        return lastvalue, figure, perts_com_pos

    def step_plot(self, figure=None, pert_counter=0, exp_data=True, last_step=None):
        """
        Plots only the reaction after perturbation with the last CoM position as the origin. 
        """

        if figure is None:
            figure = plt.figure(4)
            ax = figure.add_subplot(1, 1, 1)
        else:
            ax = figure.axes[0]
        
        # Plot the origin
        ax.plot(0, 0, 'ok', markersize=10)

        # Compensate the final step position
        # Note: for experimental data step1 is X-Data where for model data this is Y-Data
        compensated_step1 = self.step_pos[0][0] - self.com_pos[0][0]
        compensated_step2 = self.step_pos[1][0] - self.com_pos[1][0]

        # Compensate the last step position
        if last_step is not None:
            compensated_laststep1 = last_step[0] - self.com_pos[1][0]
            compensated_laststep2 = last_step[1] - self.com_pos[0][0]
        
        # Plot steps
        if exp_data is True:
            ax.plot(compensated_step1, compensated_step2,
            'o', markersize=8, markerfacecolor=(1,1,1,0),
            markeredgewidth=3, markeredgecolor=self.colors[pert_counter], label= 'Experimental step position %i' %pert_counter)
        else:
            ax.plot(compensated_step2, compensated_step1,
            'v', markeredgecolor=self.colors[pert_counter],
            markersize=10, markerfacecolor=(1,1,1,0))
            ax.plot(compensated_laststep1, compensated_laststep2,
            'v', markeredgecolor=self.colors[pert_counter],
            markersize=10, markerfacecolor=(1,1,1,0))

        return figure, self.step_pos[0][0], self.step_pos[1][0]


    def exp_plot(self , figure, pert_counter):
        """
        =INPUT=
            figure          - figure that the experimental data must be added to (data can't be plotted in a non existing figure)
            pert_counter    - keeps track of which color to give to the plotted data
        
        """
        #Experimental step positions
        ax = figure.axes[0]

        ax.plot(self.step_pos[0], self.step_pos[1], 'o',
                markersize=8, markerfacecolor=(1, 1, 1, 0), markeredgewidth=3, markeredgecolor=self.colors[pert_counter])

        #Experimental com positions
        ax.plot(self.com_pos[0], self.com_pos[1], 'x',
                markersize=10, markerfacecolor=self.colors[pert_counter], markeredgecolor=self.colors[pert_counter])

        return


    def exp_cop_plot(self,figure, pert_counter, event_counter):
        """
        =INPUT=
            figure          - figure that the CoP data must be plotted in (new figure)
            pert_counter    - keeps track of which color to give to the plotted data (based on perturbation)
            event_counter   - keeps track of which marker to give to the plotted data (based on event)
        =OUTPUT=
            figure          - returns the current figure so that the forloop can add new data to it
        =NOTES=
            Events can be found in the readme.md included with the Experimental Data
        """

        if figure is None:
            figure = plt.figure(1)
            ax = figure.add_subplot(1, 1, 1)
        else:
            ax = figure.axes[0]

        # Events
        events = ('Prt start', 'Prt end', 'Heel-strike r', 'Toe-off r', 'Heel-strike l', 'Toe-off l')

        # Experimental cop data
        ax.plot(self.cop_pos[0], self.cop_pos[1], 
                self.markers[event_counter], markeredgecolor= self.colors[pert_counter],
                markersize=10, markerfacecolor=(1, 1, 1, 0), label='%s prt' % events[event_counter])

        return figure

    def cost_plot(self, figure=None):
        """
        Function to plot the cost analysis over the full gait.
        All seperate costs will be plotted in the same figure as well as the combined costs. 
        """

        if figure is None:
            figure = plt.figure(2)
            ax = figure.add_subplot(1,1,1)
        else:
            ax = figure.axes[0]


        # Take the already excisting data
        step_nrs = self.storage.cost_landscape_fullgait['step_number']
        ankle_cost_ap = SimulationSettings.gain_ankle_cost_ap*np.asarray(self.storage.cost_landscape_fullgait['ankle_cost_ap'])
        ankle_cost_ml = SimulationSettings.gain_ankle_cost_ml*np.asarray(self.storage.cost_landscape_fullgait['ankle_cost_ml'])
        swing_cost_ap = SimulationSettings.gain_swing_cost_ap*np.asarray(self.storage.cost_landscape_fullgait['swing_cost_ap'])
        swing_cost_ml = SimulationSettings.gain_swing_cost_ml*np.asarray(self.storage.cost_landscape_fullgait['swing_cost_ml'])
        sts_cost = SimulationSettings.gain_sts_cost*np.asarray(self.storage.cost_landscape_fullgait['sts_cost'])

        # Add all costs 
        full_cost = (ankle_cost_ap + ankle_cost_ml + swing_cost_ap + swing_cost_ml + sts_cost)

        # Plot all costs
        ax.plot(step_nrs, ankle_cost_ap, 'g', label='ankle costs ap')
        ax.plot(step_nrs, ankle_cost_ml, 'g', linestyle='dashed', label='ankle costs ml')
        ax.plot(step_nrs, swing_cost_ap, 'b', label='swing costs ap')
        ax.plot(step_nrs, swing_cost_ap, 'b', linestyle='dashed', label='swing costs ml')
        ax.plot(step_nrs, sts_cost, 'r', label='sts costs')
        ax.plot(step_nrs, full_cost, 'k', label= 'full cost with gain')

        return figure          
                        

    def pert_plot(self, figure, pert_counter, last_step, last_com, exp_x, exp_y):

        if figure is None:
            figure = plt.figure(5)
            ax = figure.add_subplot(1, 1, 1)
        else:
            ax = figure.axes[0]
        
        # Plot the origin
        ax.plot(0, 0, 'ok', markersize=10)

        # Plot the last step
        latest_step = np.subtract(last_step, last_com)
        ax.plot(latest_step[0],latest_step[1], '^', markeredgecolor='b', markersize=10, markerfacecolor=(1,1,1,0))

        # Plot the perturbations CoP's
        cop_x = self.cop_pos[1] - last_com[0]
        cop_y = self.cop_pos[0] - last_com[1]
        ax.plot(cop_x, cop_y, '+', markeredgecolor=self.colors[pert_counter], markersize=10, markeredgewidth=3)

        # Plot the perturbations CoM's
        com_x = self.com_pos[1] - last_com[0]
        com_y = self.com_pos[0] - last_com[1]
        ax.plot(com_x, com_y, 'ok', markersize=10)
        ax.plot(com_x, com_y, 'x', markeredgecolor=self.colors[pert_counter], markersize=10)

        # Plot the perturbations step
        step_x = self.step_pos[1] - last_com[0]
        step_y = self.step_pos[0] - last_com[1]
        ax.plot(step_x, step_y, '^', markeredgecolor=self.colors[pert_counter], markersize=10, markerfacecolor=(1,1,1,0), markeredgewidth=3)

        # Plot the experimental data
        exp_step_x = exp_x - last_com[0]
        exp_step_y = exp_y - last_com[1]
        ax.plot(exp_step_x, exp_step_y, 'o', markeredgecolor=self.colors[pert_counter], markersize=10, markerfacecolor=(1,1,1,0), markeredgewidth=3)

        return figure

        
    def step_specific_cost_plot(self, step_number, figure=None):
        """
        =INPUT=
            step_number = user input -> which step the user wants to observe the cost of
            cop_number = user input -> with what cop value does the user want to do this
            figure = figure it needs to plot in (initialised to take a new figure)
        =OUTPUT=
            figure
        """
        #TODO: uitzoeken waarom hier nog zoveel nutteloze listen omheen zitten
        ankle_cost_ap = self.storage.cost_landscape_specificstep['ankle_cost_ap'][0]
        ankle_cost_ml = self.storage.cost_landscape_specificstep['ankle_cost_ml'][0]
        swing_cost_ap = self.storage.cost_landscape_specificstep['swing_cost_ap'][0]
        swing_cost_ml = self.storage.cost_landscape_specificstep['swing_cost_ml'][0]
        sts_cost = self.storage.cost_landscape_specificstep['sts_cost'][0][0]

        horizon = np.linspace(
            SimulationSettings.t_step, SimulationSettings.t_horizon, int(SimulationSettings.t_horizon / SimulationSettings.t_step))

        for i in range(len(ankle_cost_ap)): #TODO: Now used ankle_cost as counter for how many different units there are
            nr_of_subplots = len(ankle_cost_ap)
            if nr_of_subplots == 1:
                rows =1
            else:
                rows = 2

            #TODO: add way to not use swing cost ap but a general swing cost gain
            full_cost = (
                SimulationSettings.gain_ankle_cost_ap * np.asarray(ankle_cost_ap[i])+
                SimulationSettings.gain_ankle_cost_ml * np.asarray(ankle_cost_ml[0])+
                SimulationSettings.gain_swing_cost_ap * np.asarray(swing_cost_ap[i])+
                SimulationSettings.gain_swing_cost_ml * np.asarray(swing_cost_ml[0])+
                SimulationSettings.gain_sts_cost * np.asarray(sts_cost[i]))

            idx_min_cost = np.argmin(full_cost)
            t_min = horizon[idx_min_cost]
            y_min = full_cost[idx_min_cost]

            if figure is None:
                figure = plt.figure(3)
                ax = figure.add_subplot(rows,m.ceil(nr_of_subplots/rows),i+1)

                ax.plot(horizon, ankle_cost_ap[i], 'g', label='ankle cost ap')
                ax.plot(horizon, ankle_cost_ml[0], 'g', linestyle='dashed', label='ankle cost ml')
                ax.plot(horizon, swing_cost_ap[i], 'b', label='swing cost ap')
                ax.plot(horizon, swing_cost_ml[0], 'b', linestyle='dashed', label='swing cost ml')
                ax.plot(horizon, sts_cost[i], 'r', label='sts cost')
                ax.plot(horizon, full_cost, 'k', label='full costs with gain')
                ax.plot(t_min, y_min, '+', markerfacecolor='r', markersize=8, label='minimal cost')
            else:
                ax = figure.add_subplot(rows,m.ceil(nr_of_subplots/rows),i+1)

                
                ax.plot(horizon, ankle_cost_ap[i], 'g')
                ax.plot(horizon, ankle_cost_ml[0], 'g', linestyle='dashed')
                ax.plot(horizon, swing_cost_ap[i], 'b')
                ax.plot(horizon, swing_cost_ml[0], 'b', linestyle='dashed')
                ax.plot(horizon, sts_cost[i], 'r')
                ax.plot(horizon, full_cost, 'k')
                ax.plot(t_min, y_min, '+', markerfacecolor='r', markersize=8)

            ax.text(t_min, y_min, '({})'.format(y_min), color='white', weight='bold' )

        return figure


    def show_plot(self, figure, x_lim, y_lim, y_label, x_label, title, backgroundcolor=(0.827, 0.827, 0.827), legend=False):
        """
        =INPUT=
        figure:
            The figure created in plot
        _lim:
            array with max and min axis value
        _label:
            string that will become axis label
        title:
            string that will become figure title
        backgroundcolor:
            array of RGB 0-1 values
            initialised to be white (1,1,1)

        =NOTES=
        Legend is now overly full, however does show what marker/color is what
        TODO: find way to create more generalized legend
        """
        for i in range(len(figure.axes)):
            ax = figure.axes[i]
            subplottitles = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

            if len(figure.axes) != 1:
                figure.suptitle(title)
                ax.set_title(subplottitles[i])

            else:
                ax.set_title(title)

            #Add figure labels
            ax.set_ylabel(y_label)
            ax.set_xlabel(x_label)

            #Add axis definitions
            ax.set_ylim(y_lim)
            ax.set_xlim(x_lim)

            #Change background color
            ax.set_facecolor(backgroundcolor)

            #Add gridlines
            ax.grid()

            #Show figure
            figure.show()
            
        return