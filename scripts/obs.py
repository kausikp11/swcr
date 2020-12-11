#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range

pub = None

def main():
    global pub,right,front,fright,left,fleft
    right = 0
    fright = 0 
    front = 0 
    fleft = 0
    left = 0 
    regions = {'right':right,'fright':fright,'front':front,'fleft':left,'left':left}
    rospy.init_node('swcr',anonymous=True)
    pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
    sub1 = rospy.Subscriber("/sonar1",Range,callback1)
    sub2 = rospy.Subscriber("/sonar2",Range,callback2)
    sub3 = rospy.Subscriber("/sonar3",Range,callback3)
    sub4 = rospy.Subscriber("/sonar4",Range,callback4)
    sub5 = rospy.Subscriber("/sonar5",Range,callback5)
    print("In main")
    rospy.spin()
        
    
def callback1(msg):
    right = msg.range
    print(right)
def callback2(msg):
    fright = msg.range
def callback3(msg):
    front = msg.range
def callback4(msg):
    fleft = msg.range
def callback5(msg):
    left = msg.range
    regions = {'right':right,'fright':fright,'front':front,'fleft':fleft,'left':left}
    print(regions)
    take_action(regions)
        
	
def take_action(regions):
    msg = Twist()
    linear_x = 0
    angular_z = 0
    dist = 0.25
    state_description = ''

    if regions['front'] > dist and regions['fleft'] > dist and regions['fright'] > dist:
        state_description = 'case 1 - nothing'
        linear_x = 0.3
        angular_z = 0
    elif regions['front'] < dist and regions['fleft'] > dist and regions['fright'] > dist:
        state_description = 'case 2 - front'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] > dist and regions['fleft'] > dist and regions['fright'] < dist:
        state_description = 'case 3 - fright'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] > dist and regions['fleft'] < dist and regions['fright'] > dist:
        state_description = 'case 4 - fleft'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < dist and regions['fleft'] > dist and regions['fright'] < dist:
        state_description = 'case 5 - front and fright'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] < dist and regions['fleft'] < dist and regions['fright'] > dist:
        state_description = 'case 6 - front and fleft'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < dist and regions['fleft'] < dist and regions['fright'] < dist:
        state_description = 'case 7 - front and fleft and fright'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] > dist and regions['fleft'] < dist and regions['fright'] < dist:
        state_description = 'case 8 - fleft and fright'
        linear_x = 0
        angular_z = -0.3
    else:
        state_description = 'unknown case'

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z =  angular_z
    pub.publish(msg)
     


if __name__ == '__main__':
    main()
    