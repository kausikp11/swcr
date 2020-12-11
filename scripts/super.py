#!/usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
from math import radians,degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point,Twist
import time
ac=actionlib.SimpleActionClient("move_base",MoveBaseAction)
def move_to_goal(xGoal,yGoal):
	rospy.on_shutdown(shutdown)
	while not rospy.is_shutdown():
		while not ac.wait_for_server(rospy.Duration.from_sec(5.0)):
			rospy.loginfo("Waiting for the move_base action server to come up")
	        goal = MoveBaseGoal()   
	           #set up the frame parameters
	        goal.target_pose.header.frame_id = "map"
	        goal.target_pose.header.stamp = rospy.Time.now()
	           # moving towards the goal*/
	        goal.target_pose.pose.position =  Point(xGoal,yGoal,0)
	        goal.target_pose.pose.orientation.x = 0.0
	        goal.target_pose.pose.orientation.y = 0.0
	        goal.target_pose.pose.orientation.z = 0.0
	        goal.target_pose.pose.orientation.w = 1.0
	        rospy.loginfo("Sending goal location ...")
	        ac.send_goal(goal)
	        ac.wait_for_result(rospy.Duration(60))
	        if(ac.get_state() ==  GoalStatus.SUCCEEDED):
	            rospy.loginfo("You have reached the destination")
	            return True
	        else:
	            rospy.loginfo("The robot failed to reach the destination")
	            return False
def shutdown():
        rospy.loginfo("Stopping the robot...")
        ac.cancel_goal()
        cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
       
        rospy.sleep(2)
        cmd_vel_pub.publish(Twist())
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        rospy.init_node('map_navigation', anonymous=False)
        print'start go to goal'
        move_to_goal(-5.07385444641,-3.14828658104)
        time.sleep(10)
        move_to_goal(-1.88173961639,6.10837936401)
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("AMCL navigation test finished.")


