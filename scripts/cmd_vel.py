#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from swcr.msg import sensor

pub = None

def main():
    global pub
    right = 0
    fright = 0 
    front = 0 
    fleft = 0
    left = 0 
    regions = {'right':right,'fright':fright,'front':front,'fleft':left,'left':left}
    rospy.init_node('swcr',anonymous=True)
    pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
    take_action(regions)
    #sub = rospy.Subscriber("/sonar",sensor,callback)
    #rospy.spin()
        
    
def callback(msg):
    left = msg.l
    fleft = msg.fl
    front = msg.fm
    fright = msg.fr
    right = msg.r
    regions = {'right':right,'fright':fright,'front':front,'fleft':fleft,'left':left}
    print(regions)
    msg = Twist()
    msg.linear.x = 0.5
    msg.angular.z = 0.3
    pub.publish(msg)
    #take_action(regions)
        
	
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
    r = rospy.Rate(30) #specify rate in Hz based upon your desired PID sampling time, i.e. if desired sample time is 33ms specify rate as 30Hz
    while not rospy.is_shutdown():
        #e_drone.pid()
        main()
        r.sleep()