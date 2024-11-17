import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from matplotlib import pyplot as plt

class Plotting(object):

    def __init__(self):
        self.fig = plt.figure()
        self.axis = self.fig.add_axes([0.07, 0.05, 0.9, 0.9])

        self.x_val = []
        self.x_time = [0]

    def start_plot(self, data):
        print(data)
        self.axis.set_xlabel('Time')
        self.axis.set_ylabel('x')
        if not self.x_val or (len(self.x_val) == 1):
            self.x_val.append(data.data[0])

        if len(self.x_val) >= 2:
            self.x_time.append(self.x_time[-1]+1)
            line, = self.axis.plot(self.x_time, self.x_val, 'r-', label='x')
            self.x_val = self.x_val[1:]
            self.x_time = self.x_time[1:]

        print(len(self.x_time), len(self.x_val))
            
        self.fig.canvas.draw()

def main():
    #import pdb; pdb.set_trace()
    plot = Plotting()
    rospy.init_node('live_plotting', anonymous=False)
    pose = rospy.Subscriber('/pose', numpy_msg(Floats), plot.start_plot)
    plt.show(block=True)

if __name__ == '__main__':
    main()
