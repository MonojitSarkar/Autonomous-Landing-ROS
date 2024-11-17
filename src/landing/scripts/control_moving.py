#!/usr/bin/env python3

"""Writing the code to make the drone track the floating platform and land on it."""

import rospy
from std_msgs.msg import Float32, Float32MultiArray
from simple_pid import PID
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Empty
from datetime import datetime

class Controller(object):
    def __init__(self):
        self.pose = rospy.Subscriber('/pose', numpy_msg(Floats), self.callback)
        self.posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size = 10)
        self.vel = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
        self.pub_land = rospy.Publisher('/drone/land', Empty, queue_size = 1)
        self.var_empty = Empty()
        self.var_bool = Bool()
        self.var_bool.data = False

        self.posctrl.publish(self.var_bool)
        self.start = datetime.now()
        self.z_setpoint = 4.5

    def callback(self, data):
        current_x, current_y, current_z, current_roll, current_pitch, current_yaw = data.data[0], data.data[1], data.data[2], data.data[3], data.data[4], data.data[5]
        #print(current_x, current_y)
        p, i, d = 1, 0.000003, 0.0

        z_range = 0.1
        z_upperpoint = self.z_setpoint + z_range
        z_lowerpoint = self.z_setpoint - z_range

        pid1 = PID(p, i, d, setpoint = self.z_setpoint)
        #z_error = z_setpoint - current_z
        #z_actuation = -z_error * p
        z_actuation = pid1(current_z)

        p_yaw, i_yaw, d_yaw = 1, 0.03, 0.5

        #import pdb; pdb.set_trace()

        yaw_setpoint = 0
        yaw_range = 0.5
        yaw_upperpoint = yaw_setpoint + yaw_range
        yaw_lowerpoint = yaw_setpoint - yaw_range

        pid_yaw = PID(p_yaw, i_yaw, d_yaw, setpoint = yaw_setpoint)
        yaw_error = yaw_setpoint - current_yaw
        yaw_actuation = pid_yaw(current_yaw)

        x_setpoint = 0
        x_range = 0.01
        x_upperpoint = x_setpoint + x_range
        x_lowerpoint = x_setpoint - x_range

        px, ix, dx = 9, 0.5, 0.5
        pid2 = PID(px, ix, dx, setpoint = x_setpoint)
        #pid2.output_limits = (-0.05, 0.05)

        x_error = x_setpoint - current_x
        #x_actuation = x_error * px
        x_actuation = pid2(current_y)

        y_setpoint = 0
        y_range = 0.01
        y_upperpoint = y_setpoint + y_range
        y_lowerpoint = y_setpoint - y_range

        py, iy, dy = 7, 0.5, 0.5
        pid3 = PID(py, iy, dy, setpoint = x_setpoint)
        #pid3.output_limits = (-0.05, 0.05)

        y_error = y_setpoint - current_y
        #y_actuation = y_error * py
        y_actuation = pid3(current_x)


        
        if current_z > z_lowerpoint and current_z < z_upperpoint:
            #self.parrot_hold()

            if current_y > y_lowerpoint and current_y < y_upperpoint:

                if current_x > x_lowerpoint and current_x < x_upperpoint:
                    print('Drone at perfect height, x and y')
                    
                    if (current_yaw > 3.0 and current_yaw < 3.2) or (current_yaw > -3.2 and current_yaw < -3.0):
                        
                        print(yaw_lowerpoint, current_yaw, yaw_upperpoint)
                        print('perfect')
                        
                        if (datetime.now() - self.start).seconds > 5 :
                            self.z_setpoint -= 0.5

                        if self.z_setpoint == 2.5:
                            self.pub_land.publish(self.var_empty)
                            time = (datetime.now() - self.start).seconds
                            print('Landing Time: ' + str(time))
                    else:
                        #print(yaw_lowerpoint, current_yaw, yaw_upperpoint)
                        self.parrot_adjust(yaw_actuation, command = 'yaw')

                else:
                    self.parrot_adjust(y_actuation, command = 'y')

            else:
                self.parrot_adjust(x_actuation, command = 'x')

        else:
            self.parrot_adjust(z_actuation, command = 'z')

        """if current_yaw > yaw_lowerpoint and current_yaw < yaw_upperpoint:
                    print("Perfect Yaw")

        else:
            self.parrot_adjust(yaw_actuation, command='yaw')"""


    def parrot_hold(self):
        print('Drone in Hover mode')
        
        var_twist = Twist()
        var_twist.linear.x = 0
        var_twist.linear.y = 0
        var_twist.linear.z = 0
        var_twist.angular.x = 0
        var_twist.angular.y = 0
        var_twist.angular.z = 0

        self.vel.publish(var_twist)

    def parrot_adjust(self, actuation, command):
        print("Adjusting the drone")
        print(actuation, command)
        
        var_twist = Twist()

        if command == 'x':
            var_twist.linear.x = actuation
        elif command == 'z':
            var_twist.linear.z = actuation
        elif command == 'y':
            var_twist.linear.y = actuation
        elif command == 'yaw':
            var_twist.angular.z = actuation
        
        self.vel.publish(var_twist)

def main():
    rospy.init_node('height_check', anonymous=True)
    controller = Controller()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
