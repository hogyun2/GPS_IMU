#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Pose
from sensor_msgs.msg import MagneticField
from nav_msgs.msg import Odometry
#define

X_OFFSET = 0.105
Y_OFFSET = 0.230
#Z_OFFSET = 0.136
PI = 3.141592

p = Odometry()
def msgCallback(data):
   
    p.pose.pose.position.y = float(data.latitude)
    p.pose.pose.position.x = float(data.longitude)
    print("x:",p.pose.pose.position.x)
    print("y:",p.pose.pose.position.y)
    print("yaw:",p.pose.pose.orientation.x)
    pub.publish(p)
    
    

def msgCallback2(data):
    
    magnetX = data.magnetic_field.x
    magnetY = data.magnetic_field.y
    #magnetZ = data.magnetic_field.z
    
    magnetX-=X_OFFSET
    magnetY-=Y_OFFSET
    #magnetZ-=Z_OFFSET
    
    theta = math.atan(magnetY/magnetX)*180/PI;
    
    if magnetX>0:
        if magnetY>0:
            theta+=270
        elif magnetY<0:
            theta+=270
    if magnetX<0:
        if magnetY>0:
            theta+=90
        elif magnetY<0:
            theta+=90
    p.pose.pose.orientation.x = theta
    #print("x:",magnetX)
    #print("y:",magnetY)

def msgCallback3(data):
    pirnt(p.pose.pose.orientation.y)
    
    

pub = rospy.Publisher('/pose', Odometry, queue_size = 1)
rospy.init_node("Position_Node",anonymous=True)
rate = rospy.Rate(100)

rospy.Subscriber('/gps_data/fix',NavSatFix,msgCallback)
rospy.Subscriber('/imu/mag',MagneticField,msgCallback2)
rospy.Subscriber('/lane',Odometry,msgCallback3)
rospy.spin()






