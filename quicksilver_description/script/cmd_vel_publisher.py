#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def talker():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('cmd_vel_publisher', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        msg=Twist()
        msg.linear.x = 0.5
        msg.linear.y = 0.5
        msg.angular.z = 0.5
        rospy.loginfo(str(msg))
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass