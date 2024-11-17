#!/usr/bin/env python3

import rospy
from simple_pid import PID
from geometry_msgs.msg import Twist, Pose

class Controller(object):
    def __init__(self):
        self.pose = rospy.Subscriber('/drone/gt_pose', Pose, self.callback)
        self.vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)



    def callback(self, data):
        current_x, current_y = data.position.x, data.position.y

        x_setpoint = 0
        x_range = 0.1
        x_upperpoint = x_setpoint + x_range
        x_lowerpoint = x_setpoint - x_range

        px, ix, dx = 1, 0.5, 0
        pid2 = PID(px, ix, dx, setpoint = x_setpoint)
        #pid2.output_limits = (-1, 1)

        x_error = x_setpoint - current_x
        #x_actuation = x_error * px
        x_actuation = pid2(current_x)

        y_setpoint = 0
        y_range = 0.1
        y_upperpoint = y_setpoint + y_range
        y_lowerpoint = y_setpoint - y_range

        py, iy, dy = 1, 0.5, 0
        pid3 = PID(py, iy, dy, setpoint = y_setpoint)
        #pid3.output_limits = (-1, 1)

        y_error = y_setpoint - current_y
        #y_actuation = y_error * py
        y_actuation = pid3(current_y)

        print(x_lowerpoint, current_x, y_upperpoint)
        print(y_lowerpoint, current_y, y_upperpoint)

        """if current_y > y_lowerpoint and current_y < y_upperpoint:
            #self.parrot_hold()
            print('Drone is at the required position')
        else:
            self.parrot_adjust(y_actuation, command='y')"""


        if current_x > x_lowerpoint and current_x < x_upperpoint:
            #self.parrot_hold()

            if current_y > y_lowerpoint and current_y < y_lowerpoint:
                #self.parrot_hold()
                print('Drone is at the required position')
            else:
                self.parrot_adjust(y_actuation, command='y')

        else:
            self.parrot_adjust(x_actuation, command = 'x')

    def parrot_hold(self):
        print('Drone in Hover mode')

        var_twist = Twist()
        var_twist.linear.x = 0
        var_twist.linear.y = 0
        var_twist.linear.z = 0

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
