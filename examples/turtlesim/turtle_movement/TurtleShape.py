#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import tf.transformations  # Import transformations module
from geometry_msgs.msg import TransformStamped  # Import TransformStamped message type
from tf2_msgs.msg import TFMessage  # Import TFMessage
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class TurtleShape:
    def __init__(self):
        rospy.init_node('snake_game')
        rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.checkpoint_publisher = rospy.Publisher("/turtle1/checkpoint", String, queue_size=10)
        self.transform_publisher = rospy.Publisher("/tf", TFMessage, queue_size=10)  # Initialize TFMessage publisher
        self.pose = Pose()
        self.rate = rospy.Rate(60)
        self.direction = Twist()

    def publish_transform(self):
        # Create and publish the transform message
        transform = TransformStamped()
        transform.header.stamp = rospy.Time.now()
        transform.header.frame_id = "world"
        transform.child_frame_id = "turtle"
        transform.transform.translation.x = self.pose.x
        transform.transform.translation.y = self.pose.y
        transform.transform.translation.z = 0
        quaternion = tf.transformations.quaternion_from_euler(0, 0, self.pose.theta)
        transform.transform.rotation.x = quaternion[0]
        transform.transform.rotation.y = quaternion[1]
        transform.transform.rotation.z = quaternion[2]
        transform.transform.rotation.w = quaternion[3]

        # Create a TFMessage and add the transform
        tf_message = TFMessage([transform])
        self.transform_publisher.publish(tf_message)
        print(f"Published transform: {tf_message}")


    def pub_checkpoint(self, i):
        data = f"reached {i}"
        self.checkpoint_publisher.publish(data)
        print(f"Published checkpoint {i} with data {data}")
    
    def update_pose(self, data):
        self.pose = data

    def move_forward(self, speed=1, distance=5):
        self.direction.linear.x = speed
        time_to_move = distance / speed
        move_time = rospy.Time.now()
        
        while rospy.Time.now() - move_time < rospy.Duration(time_to_move):
            self.pub.publish(self.direction)
            self.rate.sleep()
        
        self.direction.linear.x = 0.0
        self.pub.publish(self.direction)
    
    def rotate_half_pi(self, speed=0.25):
        target_angle = self.pose.theta + math.pi/2

        if target_angle > math.pi:
            target_angle -= 2 * math.pi

        while abs(target_angle - self.pose.theta) > 0.002:
            self.direction.linear.x = 0.0

            if abs(target_angle - self.pose.theta) <= 0.05:
                self.direction.angular.z = speed/10
            elif abs(target_angle - self.pose.theta) <= 0.1:
                self.direction.angular.z = speed/5
            else:
                self.direction.angular.z = speed

            self.pub.publish(self.direction)
            self.rate.sleep()
        
        self.direction.angular.z = 0.0
        self.pub.publish(self.direction)


    def move(self, speed=1, length=1):
        pass