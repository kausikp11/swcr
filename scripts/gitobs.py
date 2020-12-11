#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Range
from geometry_msgs.msg import Twist

class SWCR():
    def __init__(self):
        self.right = 0
        self.fright = 0 
        self.front = 0 
        self.fleft = 0
        self.left = 0 
        self.regions = {'right':self.right,'fright':self.fright,'front':self.front,'fleft':self.left,'left':self.left}
        rospy.init_node('swcr',anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
        self.sub1 = rospy.Subscriber("/sonar1",Range,self.clbk_sonar1)
        self.sub2 = rospy.Subscriber("/sonar2",Range,self.clbk_sonar2)
        self.sub3 = rospy.Subscriber("/sonar3",Range,self.clbk_sonar3)
        self.sub4 = rospy.Subscriber("/sonar4",Range,self.clbk_sonar4)
        self.sub5 = rospy.Subscriber("/sonar5",Range,self.clbk_sonar5)

    
    def clbk_sonar1(self,msg):
        self.left = msg.range

    def clbk_sonar2(self,msg):
        self.fleft = msg.range

    def clbk_sonar3(self,msg):
        self.front = msg.range

    def clbk_sonar4(self,msg):
        self.fright = msg.range

    def clbk_sonar5(self,msg):
        self.right = msg.range
	
    def take_action(self,regions):
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
        self.pub.publish(msg)

    def main(self):
        self.regions = {'right':self.right,'fright':self.fright,'front':self.front,'fleft':self.fleft,'left':self.left}
        self.take_action(self.regions)


if __name__ == '__main__':
    swcr = SWCR()
    while not rospy.is_shutdown():
        swcr.main()
        rospy.Rate(30).sleep