import rospy
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats
from matplotlib import pyplot as plt

i = 0
x_val = [0] * 200
x = range(200)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 200])
ax.set_ylim([-1, 1])

line, = ax.plot(x_val, 'r-')

def plotData(value): 
    global x_val, i
    x_val[i] = value
    line.set_ydata(x_val)
    line.set_xdata(x)
    i += 1
    fig.canvas.draw()

def callBack(data):
    x_value = data.data[0]
    plotData(x_value)

def listener():
    rospy.init_node('live_plotting', anonymous=False)
    rospy.Subscriber('/pose', numpy_msg(Floats), callBack)
    plt.show(block=True)

if __name__ == '__main__':
    listener()
