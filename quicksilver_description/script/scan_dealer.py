#!/usr/bin/env python3
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan

def callback(data):
    # 创建一个新的LaserScan消息
    rospy.loginfo("I heard %s", str(data))
    new_data = LaserScan()
    new_data.header = data.header
    new_data.angle_min = data.angle_min
    new_data.angle_max = data.angle_max
    new_data.angle_increment = data.angle_increment
    new_data.time_increment = data.time_increment
    new_data.scan_time = data.scan_time
    new_data.range_min = data.range_min
    new_data.range_max = data.range_max

    # 将极坐标转换为笛卡尔坐标，进行移动，然后再转换回极坐标
    for i in range(len(data.ranges)):
        # 获取当前测量的角度和距离
        angle = data.angle_min + i * data.angle_increment
        r = data.ranges[i]

        # 将极坐标转换为笛卡尔坐标
        x = r * np.cos(angle)
        y = r * np.sin(angle)

        # 沿x轴移动0.35
        x += 0.35

        # 将笛卡尔坐标转换回极坐标
        new_r = (x**2 + y**2)**(0.5)
        new_data.ranges.append(new_r)
        new_data.intensities.append(data.intensities[i])

    # 发布新的LaserScan消息
    pub.publish(new_data)

rospy.init_node('scan_processor')
rospy.Subscriber('/scan_raw', LaserScan, callback)
pub = rospy.Publisher('/scan', LaserScan, queue_size=10)
rospy.spin()