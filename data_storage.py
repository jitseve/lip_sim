from matplotlib import pyplot as plt


class DataStorage(object):
    """
    Class to keep track of simulation data.
    Includes functionality for plotting.
    """

    def __init__(self):
        self.time = []
        self.com_pos = [[], []]
        self.com_vel = [[], []]
        self.cop_pos = [[], []]
        self.xcom_pos = [[], []]

        self.figure = None
        return

    
    def take_sample(self, time, lip_ap, lip_ml, index=None):
        com_pos_ap, com_vel_ap, cop_pos_ap, xcom_pos_ap = lip_ap.state_at(index)
        com_pos_ml, com_vel_ml, cop_pos_ml, xcom_pos_ml = lip_ml.state_at(index)
        
        self.time.append(time)
        
        self.com_pos[0].append(com_pos_ap)
        self.com_vel[0].append(com_vel_ap)
        self.cop_pos[0].append(cop_pos_ap)
        self.xcom_pos[0].append(xcom_pos_ap)
        
        self.com_pos[1].append(com_pos_ml)
        self.com_vel[1].append(com_vel_ml)
        self.cop_pos[1].append(cop_pos_ml)
        self.xcom_pos[1].append(xcom_pos_ml)
        return


    def plot(self):
        """
        Colors under the assumption that the first stance leg is left.
        Left: blue
        Right: red
        """

        self.figure = plt.figure(0)
        ax = self.figure.add_subplot(1, 1, 1)

        # Stance legs
        ax.plot(
            [self.cop_pos[1][0::2], self.com_pos[1][0::2]],
            [self.cop_pos[0][0::2], self.com_pos[0][0::2]], '-b')
        ax.plot(
            [self.cop_pos[1][1::2], self.com_pos[1][1::2]],
            [self.cop_pos[0][1::2], self.com_pos[0][1::2]], '-r')

        # Stepping legs
        ax.plot(
            [self.cop_pos[1][2::2], self.com_pos[1][1:-2:2]],
            [self.cop_pos[0][2::2], self.com_pos[0][1:-2:2]], '-b')
        ax.plot(
            [self.cop_pos[1][1::2], self.com_pos[1][0::2]],
            [self.cop_pos[0][1::2], self.com_pos[0][0::2]], '-r')

        # COM position
        ax.plot(self.com_pos[1], self.com_pos[0], 'ok', markersize=10)

        # Foot positions
        ax.plot(self.cop_pos[1][1::2], self.cop_pos[0][1::2], 'o',
            markersize=8, markerfacecolor=(1, 1, 1, 0), markeredgecolor='r')
        ax.plot(self.cop_pos[1][0::2], self.cop_pos[0][0::2], 'o',
            markersize=8, markerfacecolor=(1, 1, 1, 0), markeredgecolor='b')

        # XCOM position 
        # ax.plot(self.xcom_pos[1], self.xcom_pos[0], 'xm')

        ax.set_xlim([-0.2, 0.2])
        ax.set_aspect('equal')

        plt.show()
        return