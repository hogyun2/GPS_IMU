#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Pose
from sensor_msgs.msg import MagneticField
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32
#define

X_OFFSET = 0.105
Y_OFFSET = 0.230
#Z_OFFSET = 0.136
PI = 3.141592
state=0
p = Odometry()
def msgCallback(data):
    print("get GPS")
    p.pose.pose.position.y = float(data.latitude)
    p.pose.pose.position.x = float(data.longitude)
    print("x:",p.pose.pose.position.x)
    print("y:",p.pose.pose.position.y)
    print("yaw:",p.pose.pose.orientation.x)
    print("state:",p.pose.pose.orientation.y)
    pub.publish(p)
    
    
def msgcallback3(data):
    # print(data)
    p.pose.pose.orientation.z = float(data.data)

def msgCallback4(data):

    if(data.data==0) :
        p.pose.pose.orientation.y = data.data
    else :
        if(p.pose.pose.orientation.z==1) :
            p.pose.pose.orientation.y = p.pose.pose.orientation.z
        else :
            p.pose.pose.orientation.y = data.data

    print("x:",p.pose.pose.position.x)
    print("y:",p.pose.pose.position.y)
    print("yaw:",(p.pose.pose.orientation.x+360)%360)
    print("state:",p.pose.pose.orientation.y)

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
    p.pose.pose.orientation.x = theta+12
    #print("x:",magnetX)
    #print("y:",magnetY)
    
    

pub = rospy.Publisher('/pose', Odometry, queue_size = 1)
rospy.init_node("Position_Node",anonymous=True)
rate = rospy.Rate(100)
print('start')
rospy.Subscriber('/imu/mag',MagneticField,msgCallback2)
rospy.Subscriber('/yololo', Int32,msgcallback3)
rospy.Subscriber('/gps_data/fix',NavSatFix,msgCallback)
rospy.Subscriber('/driving_state',Int32,msgCallback4)

rospy.spin()






