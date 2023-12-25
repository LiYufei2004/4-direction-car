#!/usr/bin/python3

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

class JoyClass:
    def __init__(self, scale=1.0, offset=0.0, deadband=0.1):
        rospy.init_node("quicksilver_node")
        # self.joy_sub = rospy.Subscriber("/joy", Joy, self.joy_callback)
        self.wheel1_pub = rospy.Publisher("/quicksilver/rim_wheel2_joint/command", Float64, queue_size=10)
        self.wheel2_pub = rospy.Publisher("/quicksilver/rim_wheel3_joint/command", Float64, queue_size=10)
        self.wheel3_pub = rospy.Publisher("/quicksilver/rim_wheel4_joint/command", Float64, queue_size=10)
        self.wheel4_pub = rospy.Publisher("/quicksilver/rim_wheel1_joint/command", Float64, queue_size=10)
        self.velocity_subscriber = rospy.Subscriber('/cmd_vel', Twist, self.velocity_callback)
        self.rate = rospy.Rate(10)
        self.x = 0
        self.y = 0
        self.z = 0

    def velocity_callback(self,msg):
        self.x = msg.linear.x
        self.y = msg.linear.y
        self.z = msg.angular.z
        wheel1 = (self.x/0.038) + (self.z /0.038)
        wheel2 = (-self.y/0.038) + (self.z / 0.038)
        wheel3 = (-self.x/0.038) + (self.z / 0.038) # 0.038 is wheel radius
        wheel4 = (self.y/0.038) + (self.z / 0.038)#angular negative due to inward placement of wheels
        self.wheel1_pub.publish(wheel4)
        self.wheel2_pub.publish(wheel1)
        self.wheel3_pub.publish(wheel2)
        self.wheel4_pub.publish(wheel3)

if __name__=="__main__":
    try:
        JoyClass()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
