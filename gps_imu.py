#!/usr/bin/env python
import rospy
import math
import tf
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Pose
from sensor_msgs.msg import MagneticField
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
import pymap3d as pm
import time

# define
magnet_OFF = [0, 0, 0]
PI = 3.141592
msg = Odometry()



# # 00,126.654965,37.448611
base_lat = 37.4514444
base_lon = 126.6609291 
base_alt = 22

# base_lat = -5116885.26421
# base_lon = 2332451.83839
# base_alt = 16.4

# #ilzamap
# base_lat = 37.449206 #37.4494466
# base_lon = 126.656222 #126.656523
# base_alt = 22.1 #55.476


def get_xy(lat, lon, alt):
    e, n, u = pm.geodetic2enu(lat, lon, alt, base_lat, base_lon, base_alt)

    return e, n, u



count = 0

# fuction
def GPS_IMU(data):

    lon = float(data.longitude) #x
    lat = float(data.latitude) #y
    alt = float(data.altitude) #z

    e, n, u = get_xy(lat, lon, alt)

    # msg.pose.pose.position.y = float(data.latitude)
    # msg.pose.pose.position.x = float(data.longitude)

    msg.pose.pose.position.x = float(n)
    msg.pose.pose.position.y = float(e)
    # msg.twist.twist.linear.x = float(time.time()) 
    #print('msg : ', msg)
    # print(msg.twist.twist.linear.x)



    print("x:",msg.pose.pose.position.x)
    print("y:",msg.pose.pose.position.y)
    #print("yaw:",msg.pose.pose.orientation.x)
    pub.publish(msg)



def IMU_Calculation(data):
    quaternion = (data.orientation.x,
        data.orientation.y,
        data.orientation.z,
        data.orientation.w)

    euler = tf.transformations.euler_from_quaternion(quaternion)

    msg.twist.twist.angular.x = euler[0]*180/PI # Pitch
    msg.twist.twist.angular.y = euler[1]*180/PI # Roll
    msg.twist.twist.angular.z = euler[2]*180/PI # Yaw
    
    # Angle detail control
    #msg.twist.twist.angular.z -= 30 ##################################################
    #msg.twist.twist.angular.z = abs(360 - msg.twist.twist.angular.z%360)

    msg.twist.twist.angular.z += 0 ##################################################
    msg.twist.twist.angular.z = msg.twist.twist.angular.z%360



################################ADD!!!!!!!!!!

    msg.pose.pose.position.z = msg.twist.twist.angular.z
    if (msg.pose.pose.position.z > 180): 
        msg.pose.pose.position.z -= 360
   
    orientation = tf.transformations.quaternion_from_euler(msg.twist.twist.angular.y*PI/180, msg.twist.twist.angular.x*PI/180, msg.pose.pose.position.z*PI/180)

    msg.pose.pose.orientation.y = orientation[0]
    msg.pose.pose.orientation.x = orientation[1]
    msg.pose.pose.orientation.z = orientation[2]
    msg.pose.pose.orientation.w = orientation[3]


############################
    
    #print("yaw:", msg.twist.twist.angular.z)


pub = rospy.Publisher('/pose', Odometry, queue_size = 1)
rospy.init_node("Position_Node",anonymous=True)
rospy.Subscriber('/gps_data/fix',NavSatFix,GPS_IMU)
rospy.Subscriber('/imu/data',Imu,IMU_Calculation)
rate = rospy.Rate(500)
rospy.spin()
